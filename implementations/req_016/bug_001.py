def most_visited_urls(visits: list, n: int) -> list:
    # bug_001 (fronteira/off-by-one): fatia em n+1, retorna uma URL a mais.
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
    return ranked[:n + 1]
