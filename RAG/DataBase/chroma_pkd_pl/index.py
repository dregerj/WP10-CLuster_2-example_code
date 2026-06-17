import pandas as pd
from Helper_CSV.prepare_csv import prepare_data
from DataBase.rag_database import build_rag_database,retrieve_context

RAG_FILE = "rag_source.csv" # File with data to use in RAG
CHROMA_PATH = "./database/chroma_pkd_pl_all_data" # Path to database created in chromaDB

CSV_FOR_TEST = "./Source/pkd.csv" #Path to CSV file for test RAG or for predict NACE (PKD) number
data = pd.read_csv(CSV_FOR_TEST,sep=';')
df = data[['nace','Description']].sample(100)

def return_RAG_predict(text):
    query = str(text)
    context = retrieve_context(query, rag_collection, top_k=3)
    return context

if __name__ == "__main__":
    df_PKD = prepare_data(RAG_FILE)
    rag_collection = build_rag_database(df_PKD, CHROMA_PATH)
    df['predict_PKD'] = df['opis'].apply(lambda x: return_RAG_predict(x))
    df.reset_index()
    df.to_csv("./Output/predict_nace_rag.csv", sep="#",encoding='utf-8')