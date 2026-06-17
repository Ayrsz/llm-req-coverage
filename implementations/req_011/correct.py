def most_frequent(items: list) -> str:
    # Lista vazia => "" por definição.
    if not items:
        return ""
    # Conta as ocorrencias preservando a ordem de primeira aparicao das chaves.
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    best = items[0]
    best_count = counts[best]
    # Percorre as chaves na ordem de insercao (= ordem de primeira ocorrencia);
    # so substitui em frequencia ESTRITAMENTE maior, preservando o empate inicial.
    for item, count in counts.items():
        if count > best_count:
            best = item
            best_count = count
    return best
