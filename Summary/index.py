from FileHelper.file_helper import process_file, validation_path
from Model.model import load_model

from conf import INPUT_PATH, INPUT_DIR, INPUT_FILENAME,MODEL_PATH,MODEL_CTX,GPU_LAYERS,OUTPUT_FILE

if __name__ == "__main__":
    validation_path(INPUT_PATH, INPUT_DIR, INPUT_FILENAME)
    llm = load_model(MODEL_PATH,MODEL_CTX,GPU_LAYERS)
    process_file(INPUT_PATH, OUTPUT_FILE, llm)