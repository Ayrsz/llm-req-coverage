def filter_by_tag(bookmarks: list, tag: str) -> list:
    # bug_005 (ramo/semântica trocada): correspondência por SUBSTRING em vez de
    # tag exata ("py" passa a casar com "python").
    if not tag:
        return []
    target = tag.lower()
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if any(target in t for t in tags):
            result.append(bm["title"])
    return result
