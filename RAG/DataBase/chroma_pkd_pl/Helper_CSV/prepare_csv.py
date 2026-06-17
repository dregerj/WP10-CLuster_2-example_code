import numpy as np
import pandas as pd
from typing import Tuple, List
from typing import List, Tuple

def prepare_data(csv_path: str) ->Tuple[List[str], List[str]]:
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    df = df[['nace','description_PL']]
    df = df.rename(columns={
        'nace': 'nace', 
        'description_PL': 'Description'
    })
    df['nace'] = df['nace'].astype(str).str.strip()
    df['Description'] = (
        df['Description']
            .str.lower()
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )
    df = df[df['Description'].str.len() > 20]
    df = df[['nace', 'Description']].dropna()

    print(f"All data: {len(df)} records (to RAG)")
    return df