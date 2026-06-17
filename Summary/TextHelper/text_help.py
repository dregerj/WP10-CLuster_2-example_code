from llama_cpp import Llama
from Prompt.prompting import create_prompt
from Model.model import get_llm_response
from conf import SYSTEM_EXTRACT, USER_EXTRACT_TEMPLATE, SYSTEM_MERGE,USER_MERGE_TEMPLATE,CHUNK_SIZE,MAX_TOKENS_FINAL,MAX_TOKENS_CHUNK,TEMPERATURE,CHUNK_OVERLAP

###
## Analize once text (Map-Reduce)
###
async def analyze_single_text(llm: Llama, text: str) -> str:
    """
    Processes a single company description:
    1. Splits it into fragments (if long)
    2. Analyzes each fragment (MAP)
    3. Merges the results (REDUCE)
    """
    text = text.strip()
    if not text:
        return "No Description"
    
    if text.upper() in ("No description", "Empty", "-", ""):
        return "No description"
    
    chunks = chunk_text(text)

    if not chunks:
        return "No Description"

    # ── KROK 1: Analiza fragmentów (MAP) ──
    partial_results = []
    for idx, chunk in enumerate(chunks, 1):
        if len(chunks) > 1:
            print(f"    Part {idx}/{len(chunks)}...")

        user_prompt = USER_EXTRACT_TEMPLATE.format(text=chunk)
        prompt = create_prompt(SYSTEM_EXTRACT, user_prompt)
        result = get_llm_response(
            llm, prompt,
            max_tokens=MAX_TOKENS_CHUNK,
            temperature=TEMPERATURE
        )

        if result and result != "Generation_error":
            partial_results.append(result)

    if not partial_results:
        return "No results"

    if len(partial_results) == 1:
        final_result = partial_results[0]
    else:
        combined = "\n---\n".join(partial_results)
        combined = combined[:2500]

        user_prompt = USER_MERGE_TEMPLATE.format(fragments=combined)
        prompt = create_prompt(SYSTEM_MERGE, user_prompt)

        final_result = get_llm_response(
            llm, prompt,
            max_tokens=MAX_TOKENS_FINAL,
            temperature=0.2
        )

    clean = final_result.replace('\n', ' | ').replace('\r', '')
    clean = clean.replace(';', ',')
    clean = ' '.join(clean.split())  

    return clean


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE,
               overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Divides text into overlapping fragments.
    Tries to divide at sentence boundaries (period/semicolon).
    """
    text = text.strip()
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            search_start = max(start, end - chunk_size // 5)
            last_period = text.rfind('.', search_start, end)
            last_semicolon = text.rfind(';', search_start, end)
            best_break = max(last_period, last_semicolon)

            if best_break > start:
                end = best_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break
        start = end - overlap

    return chunks

