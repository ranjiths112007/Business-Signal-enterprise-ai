import re

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous instructions",
    r"reveal\s+(the\s+)?system prompt",
    r"show\s+(me\s+)?your\s+hidden instructions",
    r"disregard\s+the\s+rules",
]


def is_suspicious(text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in INJECTION_PATTERNS)


def sanitize_question(text: str) -> str:
    if is_suspicious(text):
        raise ValueError("Question rejected by prompt-injection guard")
    return text.strip()
