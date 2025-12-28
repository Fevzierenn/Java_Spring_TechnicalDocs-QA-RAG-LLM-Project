import os
import json
import time
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==========================================
# 1. AYARLAR
# ==========================================
print("--- FAZ 2: RETRIEVER PERFORMANS TESTİ ---")

script_dir = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB_DIR = os.path.join(script_dir, "vector_dbs")
EVAL_SET_PATH = os.path.join(script_dir, "baeldung_qa_dataset.json")  # Önceki adımda oluşan dosya

# Test edilecek K değerleri (Hoca k parametresi istemiş)
K_VALUES = [1, 3, 5]

# Modellerin Tanimlari
EMBEDDING_MODELS_MAP = {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "bge": "BAAI/bge-small-en-v1.5"
}


# ==========================================
# 2. YARDIMCI FONKSİYONLAR
# ==========================================
def load_eval_set():
    if not os.path.exists(EVAL_SET_PATH):
        print(f"❌ HATA: '{EVAL_SET_PATH}' bulunamadı! Önce soru üretme adımını tamamla.")
        exit()
    with open(EVAL_SET_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def evaluate_db(db_path, eval_data, embed_model_name):
    print(f"\n🔎 Test Ediliyor: {os.path.basename(db_path)}")

    # DB ve Model Yükle
    embeddings = HuggingFaceEmbeddings(model_name=embed_model_name)
    db = Chroma(persist_directory=db_path, embedding_function=embeddings)

    results = {k: {"hits": 0, "recall": 0.0} for k in K_VALUES}
    total_questions = len(eval_data)

    start_time = time.time()

    for item in eval_data:
        question = item['question']
        target_source = item.get('source_article') or item.get('source_doc')

        # En genis k degeri kadar getir
        max_k = max(K_VALUES)
        retrieved_docs = db.similarity_search(question, k=max_k)

        # Retrieved kaynak isimlerini listele
        retrieved_sources = [os.path.basename(doc.metadata.get('source', '')) for doc in retrieved_docs]
        target_clean = os.path.basename(target_source)

        # Her K degeri icin hesapla
        for k in K_VALUES:
            current_retrieved = retrieved_sources[:k]
            if target_clean in current_retrieved:
                results[k]["hits"] += 1

    duration = time.time() - start_time

    # Sonuclari Yüzdeye Çevir
    print(f"   Soru Sayısı: {total_questions} | Süre: {duration:.2f}sn")
    for k in K_VALUES:
        hit_rate = results[k]["hits"] / total_questions
        print(f"   👉 Recall@{k}: {hit_rate:.2%}")

    return results


# ==========================================
# 3. MAIN
# ==========================================
if __name__ == "__main__":
    eval_data = load_eval_set()
    print(f"✅ {len(eval_data)} adet test sorusu yüklendi.")

    if not os.path.exists(VECTOR_DB_DIR):
        print("❌ Veritabanı klasörü yok. Önce create_db.py çalıştır.")
        exit()

    db_folders = [f for f in os.listdir(VECTOR_DB_DIR) if f.startswith("vector_db_")]

    for folder_name in db_folders:
        full_path = os.path.join(VECTOR_DB_DIR, folder_name)

        if "minilm" in folder_name:
            model_key = EMBEDDING_MODELS_MAP["minilm"]
        elif "bge" in folder_name:
            model_key = EMBEDDING_MODELS_MAP["bge"]
        else:
            continue

        evaluate_db(full_path, eval_data, model_key)

    print("\n🏁 --- TEST TAMAMLANDI ---")