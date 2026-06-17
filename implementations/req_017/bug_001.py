def filter_by_tag(bookmarks: list, tag: str) -> list:
    # bug_001 (condição invertida na guarda): devolve [] para tag NÃO vazia.
    if tag:
        return []
    target = tag.lower()
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if target in tags:
            result.append(bm["title"])
    return result
