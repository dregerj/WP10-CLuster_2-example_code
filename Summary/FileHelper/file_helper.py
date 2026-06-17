import time
import os
from TextHelper.text_help import analyze_single_text
from llama_cpp import Llama


def count_lines(filepath: str) -> int:
    with open(filepath, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)


def count_processed_lines(output_path: str) -> int:
    if not os.path.exists(output_path):
        return 0
    with open(output_path, 'r', encoding='utf-8-sig') as f:
        return sum(1 for line in f if line.strip())


async def  validation_path(INPUT_PATH: str, INPUT_DIR: str, INPUT_FILENAME: str):
    if not os.path.exists(INPUT_PATH):
        print(f"[BŁĄD] File doesnt exists: {INPUT_PATH}")
        if not os.path.exists(INPUT_DIR):
            os.makedirs(INPUT_DIR)
            print(f"[INFO] Directory is created '{INPUT_DIR}'. "
                  f"Put file here '{INPUT_FILENAME}'.")
        return
    
async def process_file(INPUT_PATH: str, OUTPUT_FILE: str, llm: Llama):
    # ── Liczenie linii ──
    total_lines = count_lines(INPUT_PATH)
    already_done = count_processed_lines(OUTPUT_FILE)

    print(f"[INFO] Input File: {INPUT_PATH} ({total_lines} linii)")
    print(f"[INFO] Output File:  {OUTPUT_FILE}")

    if already_done > 0:
        print(f"[INFO] Start from line:  {already_done + 1} "
              f"(Ended: {already_done})")
    processed = 0
    errors = 0
    start_time = time.time()
    write_mode = 'a' if already_done > 0 else 'w'
    with open(INPUT_PATH, 'r', encoding='utf-8') as f_in, \
         open(OUTPUT_FILE, write_mode, encoding='utf-8-sig') as f_out:
        if write_mode == 'w':
            f_out.write("Original Data;Results_AI\n")
            f_out.flush()

        for i, line in enumerate(f_in, 1):
            line = line.strip()
            if not line:
                continue
            if i <= already_done:
                continue
            elapsed = time.time() - start_time
            if processed > 0:
                avg_time = elapsed / processed
                remaining = avg_time * (total_lines - i)
                eta = f"~{remaining/60:.0f}min"
            else:
                eta = "calc..."
            print(f"\n{'='*60}")
            print(f"[{i}/{total_lines}] Procesing... (ETA: {eta})")
            print(f"  Tekst: {line[:80]}{'...' if len(line)>80 else ''}")
            try:
                line_start = time.time()
                ai_result = await analyze_single_text(llm, line)
                line_time = time.time() - line_start

                output_line = f"{line};{ai_result}\n"
                f_out.write(output_line)
                f_out.flush()

                processed += 1
                print(f"  [OK] Time: {line_time:.1f}s")
                print(f"  Result: {ai_result[:100]}{'...' if len(ai_result)>100 else ''}")

            except KeyboardInterrupt:
                print(f"\n[STOP] Break operation from user {processed}")
                print(f"[INFO] You can try use start process again")
                return

            except Exception as e:
                errors += 1
                print(f"  [Error] {type(e).__name__}: {e}")
                f_out.write(f"{line};BŁĄD: {str(e)[:50]}\n")
                f_out.flush()

    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"[KONIEC] Process is stoping")
    print(f"  Ended:  {processed} lines")
    print(f"  Errors:         {errors}")
    print(f"  Total time:   {total_time/60:.1f} min")
    if processed > 0:
        print(f"  Average time:   {total_time/processed:.1f}s / line")
    print(f"  Results are in:       {OUTPUT_FILE}")
