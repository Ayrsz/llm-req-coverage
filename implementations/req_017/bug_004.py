def filter_by_tag(bookmarks: list, tag: str) -> list:
    # bug_004 (constante/normalização errada): não normaliza a tag procurada
    # para minúsculas, tornando a correspondência case-sensitive.
    if not tag:
        return []
    target = tag
    result = []
    for bm in bookmarks:
        tags = [t.lower() for t in bm.get("tags", [])]
        if target in tags:
            result.append(bm["title"])
    return result
