def most_visited_urls(visits: list, n: int) -> list:
    # bug_002 (operador errado): ordena por frequência CRESCENTE (sem o sinal),
    # retornando as menos visitadas.
    if n <= 0:
        return []
    counts = {}
    first_seen = {}
    for i, url in enumerate(visits):
        if url not in counts:
            counts[url] = 0
            first_seen[url] = i
        counts[url] += 1
    ranked = sorted(counts, key=lambda u: (counts[u], first_seen[u]))
    return ranked[:n]
