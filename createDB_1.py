import os
import shutil
import time
import json
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma  # Guncel kutuphane
from langchain_huggingface import HuggingFaceEmbeddings  # Guncel kutuphane

# ==========================================
# 1. AYARLAR VE PATH YAPILANDIRMASI
# ==========================================
print("--- FAZ 1: VERİTABANI OLUŞTURMA MOTORU ---")

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
# Veri yolunu kendi bilgisayarina gore ayarla, ornegin script ile ayni yerdeyse:
DATA_PATH = os.path.join(script_dir, "baeldung_articles_markdown")

# Klasör yoksa oluştur (Test için)
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)
    print(f"⚠️ UYARI: '{DATA_PATH}' klasörü bulunamadı ve oluşturuldu. Lütfen .md dosyalarını buraya koy.")

# Rehberin istedigi Embedding Modelleri [cite: 29-33]
EMBEDDING_MODELS = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "bge": "BAAI/bge-small-en-v1.5"
}

# Raporlama icin sonuclari tutacagimiz sozluk
benchmark_metrics = {}


# ==========================================
# 2. DÖKÜMAN YÜKLEME VE TEMİZLEME [cite: 7, 20]
# ==========================================
def load_documents():
    print(f"\n--> Adım 1: Dosyalar okunuyor: {DATA_PATH}")
    loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8', 'autodetect_encoding': True},
        show_progress=True
    )
    docs = loader.load()
    if not docs:
        print("❌ HATA: Hiç dosya yüklenemedi! Klasör yolunu kontrol et.")
        exit()

    print(f"✅ {len(docs)} adet makale hafızaya alındı.")
    return docs


# ==========================================
# 3. CHUNKING STRATEJİLERİ [cite: 22-28]
# ==========================================
def get_chunks_strategy_fixed(docs):
    """STRATEJİ A: FIXED-LENGTH (Rehber: Fixed-length chunking)"""
    # 1000 token yaklasik 4000 karakter, overlap context kopmamasi icin onemli
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)


def get_chunks_strategy_smart(docs):
    """STRATEJİ B: SECTION-BASED (Rehber: Section-based chunking)"""
    # Markdown basliklarina gore bolme
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)

    md_header_splits = []
    for doc in docs:
        # Markdown split yapinca metadata kaybolabilir, manuel ekliyoruz
        splits = markdown_splitter.split_text(doc.page_content)
        for split in splits:
            split.metadata['source'] = doc.metadata.get('source', 'unknown')
        md_header_splits.extend(splits)

    # Basliklar cok uzunsa onlari da fixed ile boluyoruz (Hybrid yaklasim)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(md_header_splits)


# ==========================================
# 4. VEKTÖR VERİTABANI OLUŞTURUCU [cite: 38]
# ==========================================
def create_vector_db(docs, chunk_strategy, embed_model_key):
    db_name = f"vector_db_{chunk_strategy}_{embed_model_key}"
    db_folder_path = os.path.join(script_dir, "vector_dbs", db_name)

    # Chunking Islemi
    if chunk_strategy == "fixed":
        chunks = get_chunks_strategy_fixed(docs)
    else:
        chunks = get_chunks_strategy_smart(docs)

    print(f"\n------------------------------------------------")
    print(f"⚙️  OLUŞTURULUYOR: {db_name}")
    print(f"🧠 Model: {EMBEDDING_MODELS[embed_model_key]}")
    print(f"📄 Chunk Sayısı: {len(chunks)}")

    # Embedding Modelini Yukle
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODELS[embed_model_key],
        model_kwargs={'device': 'cpu'},  # GPU varsa 'cuda' yapabilirsin
        encode_kwargs={'normalize_embeddings': True}
    )

    # Rehber istegi: Embedding boyutunu kaydet
    test_embed = embeddings.embed_query("test")
    embed_dim = len(test_embed)

    # Eski DB varsa temizle
    if os.path.exists(db_folder_path):
        shutil.rmtree(db_folder_path)

    # KRONOMETRE BASLAT (Rehber: Encoding Time)
    start_time = time.time()

    # ChromaDB Olustur (Persistent)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_folder_path
    )

    end_time = time.time()
    duration = end_time - start_time

    print(f"✅ BAŞARILI.")
    print(f"⏱️  ENCODING TIME: {duration:.2f} saniye")
    print(f"📏 EMBEDDING DIM: {embed_dim}")

    # Sonuclari Rapor Icin Kaydet
    benchmark_metrics[db_name] = {
        "chunk_strategy": chunk_strategy,
        "embedding_model": embed_model_key,
        "encoding_time_sec": round(duration, 2),
        "embedding_dimension": embed_dim,
        "total_chunks": len(chunks)
    }


# ==========================================
# 5. MAIN
# ==========================================
if __name__ == "__main__":
    # Klasör yapısını hazırla
    if not os.path.exists(os.path.join(script_dir, "vector_dbs")):
        os.makedirs(os.path.join(script_dir, "vector_dbs"))

    raw_docs = load_documents()

    if raw_docs:
        # SENARYO 1: Smart Chunking + MiniLM (Hızlı, Küçük)
        create_vector_db(raw_docs, chunk_strategy="smart", embed_model_key="minilm")

        # SENARYO 2: Fixed Chunking + MiniLM (Karşılaştırma Grubu 1)
        create_vector_db(raw_docs, chunk_strategy="fixed", embed_model_key="minilm")

        # SENARYO 3: Smart Chunking + BGE (Daha iyi retrieval iddiası var)
        create_vector_db(raw_docs, chunk_strategy="smart", embed_model_key="bge")

        # Metrikleri JSON olarak kaydet (Rapor tablosu icin altin degerinde)
        with open(os.path.join(script_dir, "benchmark_metrics.json"), "w") as f:
            json.dump(benchmark_metrics, f, indent=4)

        print("\n🎉 TÜM VERİTABANLARI OLUŞTURULDU VE METRİKLER KAYDEDİLDİ!")
        print(f"📁 Dosya konumu: {os.path.join(script_dir, 'vector_dbs')}")