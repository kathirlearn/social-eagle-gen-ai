def is_low_confidence(answer: str) -> bool:
    confidence_signals = [
        "not mentioned",
        "not available",
        "no information",
        "insufficient context"
    ]
    return any(signal in answer.lower() for signal in confidence_signals)
