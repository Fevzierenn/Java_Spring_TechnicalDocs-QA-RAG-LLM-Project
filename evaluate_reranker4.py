import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import CrossEncoder
import time
import os

# --- SETTINGS ---
BASE_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\vector_dbs"
CSV_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\golden-QA.csv"

# Using our best model
BEST_DB_FOLDER = "vector_db_smart_minilm"
COLLECTION_NAME = "langchain"

# Cross-Encoder Model (Re-Ranker)
# This model takes a (Question, Answer) pair and returns a precision score between 0-1.
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# How many candidates to retrieve and re-rank?
INITIAL_K = 10
FINAL_K = 3  # Final count to be sent to the LLM

# Score Threshold - We discard results lower than this
SCORE_THRESHOLD = 0.0  # Setting to 0 for now to see the full effect, can increase later.


def load_data():
    try:
        df = pd.read_csv(CSV_PATH, sep=';', encoding='cp1252')
        df.columns = df.columns.str.strip().str.lower()
        q_col = next((c for c in df.columns if 'question' in c or 'soru' in c), None)
        s_col = next((c for c in df.columns if 'path' in c or 'source' in c), None)  # Path/Source column
        return df[[q_col, s_col]].dropna().to_dict('records')
    except Exception as e:
        print(f"CSV Error: {e}")
        return []


def evaluate_with_reranker():
    print(f"-RE-RANKER PERFORMANCE TEST -")
    print(f"Vector DB: {BEST_DB_FOLDER}")
    print(f"Re-Ranker: {RERANKER_MODEL_NAME}")

    # 1. Prepare Models
    print("Loading models...")
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    reranker = CrossEncoder(RERANKER_MODEL_NAME)

    # DB Connection
    db_path = os.path.join(BASE_PATH, BEST_DB_FOLDER)
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name=COLLECTION_NAME, embedding_function=ef)

    data = load_data()
    print(f"{len(data)} questions will be tested.\n")

    hits_at_1 = 0
    hits_at_3 = 0
    start_time = time.time()

    for item in data:
        question = item[list(item.keys())[0]]  # Question
        target_doc = os.path.basename(item[list(item.keys())[1]])  # Target filename

        # A) VECTOR SEARCH (Retrieval) - Get top 10
        results = collection.query(query_texts=[question], n_results=INITIAL_K)

        docs = results['documents'][0]
        metas = results['metadatas'][0]

        # B) RE-RANKING
        # Prepare (Question, Text) pairs for Cross-Encoder
        pairs = [[question, doc] for doc in docs]

        # Predict scores
        scores = reranker.predict(pairs)

        # Sort by scores (Highest score first)
        # Zipping and sorting: (Score, Doc, Meta)
        ranked_results = sorted(zip(scores, docs, metas), key=lambda x: x[0], reverse=True)

        # C) THRESHOLD FILTERING & SELECTION
        final_candidates = []
        for score, doc, meta in ranked_results:
            if score > SCORE_THRESHOLD:
                final_candidates.append(os.path.basename(meta.get('source', '')))

        # Take top k candidates
        top_k_candidates = final_candidates[:FINAL_K]

        # D) CHECK (Hit Check)
        # Is the target file in this list?
        # Recall@1: Is the very first item (index 0) correct?
        if len(top_k_candidates) > 0 and (target_doc in top_k_candidates[0] or top_k_candidates[0] in target_doc):
            hits_at_1 += 1

        # Recall@3: Is it anywhere in the list?
        match_found = False
        for cand in top_k_candidates:
            if target_doc in cand or cand in target_doc:
                match_found = True
                break
        if match_found:
            hits_at_3 += 1

    duration = time.time() - start_time

    print(f"\nRESULTS ({len(data)} Questions):")
    print(f"Total Time: {duration:.2f}s (Per question: {duration / len(data):.2f}s)")
    print(f"Re-Ranked Recall@1: %{(hits_at_1 / len(data)) * 100:.2f}")
    print(f"Re-Ranked Recall@3: %{(hits_at_3 / len(data)) * 100:.2f}")


if __name__ == "__main__":
    evaluate_with_reranker()