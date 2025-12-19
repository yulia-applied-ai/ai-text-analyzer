from __future__ import annotations

import json
import sys
from pathlib import Path

PROMPT_PATH = Path("analysis_prompt.txt")
DEFAULT_INPUT_PATH = Path("sample_input.txt")


def load_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError(f"File is empty: {path}")
    return text


def load_prompt(path: Path = PROMPT_PATH) -> str:
    return load_text(path)


def build_prompt(prompt_template: str, text: str) -> str:
    return f"{prompt_template}\n\n{text}\n"


def fake_llm_response(text: str) -> dict:
    lowered = text.lower()

    positive_words = ["great", "good", "love", "excellent", "amazing", "happy", "intuitive"]
    negative_words = ["bad", "slow", "hate", "terrible", "awful", "problem", "refund", "disappointing"]

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
    if "interface" in lowered or "ui" in lowered:
        key_ideas.append("User interface / usability is mentioned")
    if "feature" in lowered:
        key_ideas.append("Product features are discussed")
    if "response" in lowered or "days" in lowered:
        key_ideas.append("Response time is mentioned")

    summary = text.replace("\n", " ").strip()
    if len(summary) > 180:
        summary = summary[:177] + "..."

    return {
        "sentiment": sentiment,
        "key_ideas": key_ideas or ["General feedback"],
        "summary": summary,
    }


def analyze_text(text: str) -> dict:
    prompt_template = load_prompt()
    final_prompt = build_prompt(prompt_template, text)

    llm_output = fake_llm_response(text)

    return {
        "analysis": llm_output,
        "prompt_preview": final_prompt[:300],
    }


def analyze_file(input_path: Path) -> dict:
    text = load_text(input_path)
    result = analyze_text(text)
    result["input_file"] = str(input_path)
    return result


def main():
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = DEFAULT_INPUT_PATH

    result = analyze_file(input_path)

    # 1. Друк у термінал
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 2. Збереження у файл
    output_path = Path("result.json")
    output_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"\n✅ Result saved to {output_path}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
