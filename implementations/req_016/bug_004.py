def most_visited_urls(visits: list, n: int) -> list:
    # bug_004 (constante errada): fatia fixa em 1, ignorando n (sempre top-1).
    if n <= 0:
        return []
    counts = {}
    first_seen = {}
    for i, url in enumerate(visits):
        if url not in counts:
            counts[url] = 0
            first_seen[url] = i
        counts[url] += 1
    ranked = sorted(counts, key=lambda u: (-counts[u], first_seen[u]))
    return ranked[:1]
