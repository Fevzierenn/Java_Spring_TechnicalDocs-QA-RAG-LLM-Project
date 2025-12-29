import pandas as pd
import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from rouge_score import rouge_scorer
from tqdm import tqdm


# 1. CONFIGURATION

VECTOR_DB_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\vector_dbs\vector_db_smart_minilm"
COLLECTION_NAME = "langchain"
CSV_PATH = r"D:\LLM_PROJECT-DEEPLEARNING\golden-QA.csv"
TOP_K = 3

# Thresholds
SEMANTIC_THRESHOLD = 0.3

# 2. HELPER FUNCTIONS

def normalize_filename(path_str):
    """Extracts the filename from the path and cleans it."""
    if not isinstance(path_str, str): return ""
    return os.path.basename(path_str).strip().lower()


def check_source_match(target_path, retrieved_path):
    """Checks if the source filenames match."""
    t = normalize_filename(target_path)
    r = normalize_filename(retrieved_path)
    # Assume match if one contains the other (e.g., handling .md extensions)
    return (t in r) or (r in t)


# 3. EVALUATION ENGINE

def run_hybrid_evaluation():
    print("STARTING HYBRID RETRIEVER TEST (SOURCE + SEMANTIC)...")
    print("-" * 60)


    print("Loading database...")
    ef = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=ef, collection_name=COLLECTION_NAME)


    try:
        df = pd.read_csv(CSV_PATH, sep=';', encoding='cp1252')
        df.columns = df.columns.str.strip().str.lower()

        # Automatically find columns (checking for both English and Turkish keywords to be safe)
        q_col = next((c for c in df.columns if 'question' in c or 'soru' in c))
        a_col = next((c for c in df.columns if 'answer' in c or 'cevap' in c))
        # Path column is optional
        path_col = next((c for c in df.columns if 'path' in c or 'source' in c or 'dosya' in c), None)

        if path_col:
            data = df[[q_col, a_col, path_col]].to_dict('records')
            print(f"Loaded {len(data)} questions. (Path column found: '{path_col}')")
        else:
            print("WARNING: 'PATH' column not found! Only semantic checks will be performed.")
            data = df[[q_col, a_col]].to_dict('records')

    except Exception as e:
        print(f"CSV Error: {e}")
        return

    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    hits_1 = 0
    hits_3 = 0
    mrr_sum = 0
    logs = []
    for item in tqdm(data):
        question = item[q_col]
        ground_truth = item[a_col]
        target_source = item[path_col] if path_col else ""

        # Retriever
        docs = db.similarity_search(question, k=TOP_K)

        found_rank = -1
        is_source_match = False
        is_semantic_match = False

        # Analyze Top-K results
        best_doc_score = 0
        best_doc_source = ""

        for rank, doc in enumerate(docs):
            retrieved_source = doc.metadata.get("source", "")

            # 1. Check: Source Match (If available)
            src_match = False
            if path_col:
                src_match = check_source_match(target_source, retrieved_source)

            # 2. Check: Semantic Match (ROUGE)
            sem_score = scorer.score(ground_truth, doc.page_content)['rougeL'].fmeasure
            sem_match = sem_score >= SEMANTIC_THRESHOLD

            # Keep the best score for logging
            if rank == 0:
                best_doc_score = sem_score
                best_doc_source = retrieved_source

            # HYBRID DECISION MECHANISM
            # Logic: If Path matches -> DEFINITELY correct. If Path missing -> correct if Semantic match.
            is_hit = False
            if path_col and src_match:
                is_hit = True
                is_source_match = True
            elif sem_match:
                is_hit = True
                is_semantic_match = True

            if is_hit:
                if found_rank == -1:  # Found for the first time (for MRR)
                    found_rank = rank + 1
                    mrr_sum += (1.0 / found_rank)
                    if rank == 0: hits_1 += 1
                hits_3 += 1
                break  # Hit recorded for this question, no need to check other docs

        # Logging
        logs.append({
            "Question": question,
            "Target_Source": normalize_filename(target_source) if path_col else "-",
            "Retrieved_Source": normalize_filename(best_doc_source),
            "Source_Match": "YES" if is_source_match else "NO",
            "Semantic_Score": round(best_doc_score, 3),
            "Result": "SUCCESS" if found_rank != -1 else "FAILURE",
            "Found_At_Rank": found_rank if found_rank != -1 else "-"
        })

    # 4. RESULTS

    total = len(data)
    hr_1 = hits_1 / total
    hr_3 = hits_3 / total

    mrr = mrr_sum / total

    print("\n" + "=" * 50)
    print("A. RETRIEVER-ONLY PERFORMANCE (HYBRID RESULTS)")
    print("=" * 50)
    print(f"Total Questions: {total}")
    print("-" * 50)
    print(f"Hit Rate@1 (Recall@1): {hr_1:.4f}  ({hr_1 * 100:.1f}%)")
    print(f"Hit Rate@3 (Recall@3): {hr_3:.4f}  ({hr_3 * 100:.1f}%)")
    print(f"MRR@3 (Mean Rank): {mrr:.4f}")
    print("-" * 50)
    print("METHODOLOGY:")
    print("1. Source Match: Does the target filename exist in the retriever output?")
    print(f"2. Semantic Match: Is content similarity > {SEMANTIC_THRESHOLD}?")
    print("=" * 50)

    # Save detailed log
    pd.DataFrame(logs).to_excel("Retriever_Analysis_Detail.xlsx", index=False)
    print("Detailed analysis saved to 'Retriever_Analysis_Detail.xlsx'.")


if __name__ == "__main__":
    run_hybrid_evaluation()