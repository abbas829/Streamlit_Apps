def inject_keywords(base_caption: str, keywords: list) -> str:
    kw = ", ".join(keywords[:3])
    if len(base_caption) < 100:
        return f"{base_caption} Featuring {kw}."
    return base_caption.replace(".", f", featuring {kw}.")