###
## Build prompt
###
async def create_prompt(system: str, user: str) -> str:
    """Tworzy prompt w formacie ChatML używanym przez Bielik-Instruct."""
    return (
        f"<|im_start|>system\n{system}<|im_end|>\n"
        f"<|im_start|>user\n{user}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )

