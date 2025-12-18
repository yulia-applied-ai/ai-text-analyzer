def analyze_text(text: str) -> dict:
    """
    Analyzes input text and returns structured analysis.
    """
    result = {
        "original_text": text,
        "sentiment": "unknown",
        "key_ideas": [],
        "summary": ""
    }

    return result


if name == "__main__":
    sample_text = "The product is great, but customer support is very slow."
    analysis = analyze_text(sample_text)
    print(analysis)
