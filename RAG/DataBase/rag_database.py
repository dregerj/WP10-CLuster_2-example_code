import os
import s3fs
import pandas as pd 
import chromadb
import hashlib
from chromadb import Collection
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from tqdm import tqdm
from sentence_transformers import CrossEncoder

COLLECTION_NAME = "pkd_database" # name of collection data
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large" ##Model for embedning   Zmiana modelu na intfloat/multilingual-e5-large || sdadas/polish-roberta-base-v2 || sdadas/mmlw-e5-base
RERANKER_MODEL_NAME = "BAAI/bge-reranker-v2-gemma" # Model for reranked
RETRIEVER_K = 10 # numbers return values for reranked
RERANKER_K = 3 # Number of return final values


reranker = CrossEncoder(RERANKER_MODEL_NAME, cache_folder ="../model/")


def build_rag_database(df: pd.DataFrame, database_path: str) ->Collection:
    
    if not os.path.exists(database_path):
        os.makedirs(database_path)
    
    embedding_func = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME, cache_folder ="../model/")
    client = chromadb.PersistentClient(path=database_path)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func
    )
    
    if collection.count() == 0:
        print("Build NACE DataBase")
        batch_size = 32
        for i in tqdm(range(0, len(df), batch_size), desc="ChromaDB"):
            batch = df.iloc[i:i + batch_size].copy()
            batch = batch.dropna(subset=['Description', 'nace']).reset_index(drop=True)
            batch = batch[batch['Description'].str.strip() != ''].reset_index(drop=True)

            if len(batch) == 0:
                continue
            batch['Description'] = (
                batch['Description']
                    .str.lower()
                    .str.strip()
                    .str.replace(r"\s+", " ", regex=True)
                    
                )
            batch['nace'] = batch['nace'].astype(str)
            documents = ["passage: " + doc for doc in batch['Description'].tolist()]
            metadatas = batch[['nace']].to_dict('records')
            ids = [
                    f"{code}_{hashlib.md5(desc.encode()).hexdigest()}"
                    for code, desc in zip(batch['nace'], batch['Description'])]

            try:
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
            except Exception as e:
                print(f"\nError in batch {i//batch_size + 1} (indeksy {i}–{i+batch_size-1})")
                print(f"   Number of documents: {len(documents)}")
                print(f"   Number of metadanych: {len(metadatas)}")
                print(f"   ID`s:         {len(ids)}")
                print(f"   Error complain: {e}")
                batch.to_csv(f"./Errors/chromadb_error_batch_{i}.csv", index=False)
                continue
        print(f"Save {collection.count()} records")
    return collection


def retrieve_context(query: str, collection: Collection, top_k: int) ->str:
    reranker_k = top_k or RERANKER_K
    query_prefixed = "query: " + query

    results = collection.query(
        query_texts=[query_prefixed],
        n_results=RETRIEVER_K,
        include=["documents", "metadatas"]
    )
    
    docs = results['documents'][0]
    metas = results['metadatas'][0]

    if len(docs) == 0:
        return "No Results"
    
    clean_docs = [doc.replace("passage: ", "") for doc in docs]
    pairs = [[query, doc] for doc in clean_docs]
    scores = reranker.predict(pairs)
    
    ranked = sorted(
        zip(clean_docs, metas, scores),
        key=lambda x: x[2],
        reverse=True
    )[:reranker_k]
    parts = []
    
    for doc, meta, score in ranked:
        parts.append(f"Code of Nace(PKD): {meta['nace']}"
        )

    return "|".join(parts)