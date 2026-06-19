from pathlib import Path

# Katalog główny projektu (Summary)
BASE_DIR = Path(__file__).parent

# Katalogi
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# Pliki
INPUT_FILENAME = "input.csv"
OUTPUT_FILENAME = "WP-10_gotowe.csv"

INPUT_PATH = INPUT_DIR / INPUT_FILENAME
OUTPUT_FILE = OUTPUT_DIR / OUTPUT_FILENAME

# Model
MODEL_PATH = r'Bielik-1.5B-v3.0-Instruct.Q8_0.gguf'

MODEL_CTX = 4096
GPU_LAYERS = -1

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

MAX_TOKENS_CHUNK = 200
MAX_TOKENS_FINAL = 400

TEMPERATURE = 0.1