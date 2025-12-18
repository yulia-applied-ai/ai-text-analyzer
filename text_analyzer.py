from future import annotations

import json
from pathlib import Path


PROMPT_PATH = Path("analysis_prompt.txt")


def load_prompt(path: Path = PROMPT_PATH) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {path}. Make sure analysis_prompt.txt is in the repo root."
        )
    return path.read_text(encoding="utf-8").strip()


def build_prompt(prompt_template: str, text: str) -> str:
    # We keep prompt in a separate file and append the user text at runtime
    return f"{prompt_template}\n\n{text}\n"


def fake_llm_response(text: str) -> dict:
    """
    Temporary stub вместо LLM.
    На цьому етапі нам важлива структура пайплайна.
    """
    lowered = text.lower()

    # супер-простий "sentiment" для MVP
    positive_words = ["great", "good", "love", "excellent", "amazing", "happy"]
    negative_words = ["bad", "slow", "hate", "terrible", "awful", "problem", "refund"]

    pos = any(w in lowered for w in positive_words)
    neg = any(w in lowered for w in negative_words)

    if pos and not neg:
        sentiment = "positive"
    elif neg and not pos:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    key_ideas = []
    if "support" in lowered:
        key_ideas.append("Customer support is mentioned")
    if "product" in lowered:
        key_ideas.append("Product quality is discussed")

    summary = text.strip()
    if len(summary) > 160:
        summary = summary[:157] + "..."

    return {
        "sentiment": sentiment,
        "key_ideas": key_ideas or ["General feedback"],
        "summary": summary,
    }


def analyze_text(text: str) -> dict:
    prompt_template = load_prompt()
    final_prompt = build_prompt(prompt_template, text)

    # Поки що LLM не викликаємо — але prompt будуємо як треба
    llm_output = fake_llm_response(text)

    return {
        "input_text": text,
        "prompt_preview": final_prompt[:300],  # щоб бачити, що все правильно зібралось
        "analysis": llm_output,
    }


if name == "__main__":
    sample_text = "The product is great, but customer support is very slow."
    result = analyze_text(sample_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
