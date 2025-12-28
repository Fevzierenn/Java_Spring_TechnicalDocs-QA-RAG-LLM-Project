import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
import os

# --- SETTINGS ---
BASE_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\vector_dbs"
CSV_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\golden-QA.csv"
COMMON_COLLECTION_NAME = "langchain"

# Models to Compare
DBS_TO_COMPARE = {
    "Old (Fixed)": "vector_db_fixed_minilm",
    "New (Smart)": "vector_db_smart_minilm"
}

minilm_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def inspect_retrieval(question_text, answer_text, n_results=3):
    print(f"\n{'#' * 100}")
    print(f"QUESTION: {question_text}")
    print(f"GROUND TRUTH (Summary): {str(answer_text)[:120]}...")
    print(f"{'#' * 100}")

    for display_name, folder_name in DBS_TO_COMPARE.items():
        full_db_path = os.path.join(BASE_PATH, folder_name)
        print(f"\n   MODEL: {display_name}")
        print(f"   {'-' * 50}")

        try:
            client = chromadb.PersistentClient(path=full_db_path)
            collection = client.get_collection(name=COMMON_COLLECTION_NAME, embedding_function=minilm_ef)

            results = collection.query(
                query_texts=[question_text],
                n_results=n_results
            )

            # Loop through the results
            for i in range(n_results):
                doc = results['documents'][0][i]
                meta = results['metadatas'][0][i]
                dist = results['distances'][0][i]

                # Make reading easier
                preview_text = doc.replace('\n', ' ')[:250]  # First 250 characters

                print(f"      [Rank {i + 1} | Score: {dist:.4f}]")
                print(f"         Source: {os.path.basename(meta.get('source', 'Unknown'))}")
                print(f"         Content: \"{preview_text}...\"")
                print("      " + "." * 40)

        except Exception as e:
            print(f"      Error: {e}")


# --- EXECUTION ---
if __name__ == "__main__":
    print("Starting Top-3 Chunk Analysis...")

    try:
        df = pd.read_csv(CSV_PATH, sep=';', encoding='cp1252')
        df.columns = df.columns.str.strip().str.lower()
        q_col = next((c for c in df.columns if 'question' in c or 'soru' in c), None)
        a_col = next((c for c in df.columns if 'answer' in c or 'cevap' in c), None)

        if not q_col: raise ValueError("Question column not found!")

    except Exception as e:
        print(f"CSV Error: {e}")
        exit()

    # 3 Random Questions
    sample_df = df.sample(3)

    for index, row in sample_df.iterrows():
        inspect_retrieval(row[q_col], row[a_col] if a_col else "None")
        input("\nPress Enter to proceed to the next question...")

    print("\nAnalysis finished.")