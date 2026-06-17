import os
###
## System and User Prompts
###

SYSTEM_EXTRACT = "Wyodrębnij branżę, produkty i usługi z opisu firmy."
USER_EXTRACT_TEMPLATE = (
    "Wypisz dane z tekstu w formacie:\n"
    "Branża: [nazwa]\n"
    "Produkty: [max 5, lub 'brak']\n"
    "Usługi: [max 5, lub 'brak']\n\n"
    "Pomijaj adresy i lokalizacje.\n"
    "Jeśli tekst pusty lub 'BRAK OPISU' napisz tylko: BRAK OPISU\n\n"
    "Tekst:\n{text}"
)

SYSTEM_MERGE = "Scal dane w jeden wpis. Usuń duplikaty."

USER_MERGE_TEMPLATE = (
    "Scal w format: Branża: ... | Produkty: max 5 | Usługi: max 5\n"
    "Usuń powtórzenia.\n\n"
    "Dane:\n{fragments}"
)

# Parametry przetwarzania
CHUNK_SIZE      = 1200      # Size of the text fragment (in characters)
CHUNK_OVERLAP   = 150       # Overlay between fragments
MAX_TOKENS_CHUNK = 200      # Max tokens per fragment response
MAX_TOKENS_FINAL = 400      # Max tokens per final response
TEMPERATURE     = 0.1       # Low = more deterministic responses


INPUT_DIR       = "input"
INPUT_FILENAME  = "file_to_summarize.csv"
OUTPUT_FILE     = "summarise_text.csv"
MODEL_PATH      = r"./Models/Bielik-1.5B-v3.0-Instruct.Q8_0.gguf"

MODEL_CTX       = 4096
GPU_LAYERS      = -1

CSV_SEPARATOR   = ";"

INPUT_PATH = os.path.join(INPUT_DIR, INPUT_FILENAME)