import unicodedata


def slugify(text: str) -> str:
    # 1) Decompoe acentos (NFKD) e descarta marcas combinantes (categoria Mn).
    decomposed = unicodedata.normalize("NFKD", text)
    no_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    # 2) Minusculas.
    lowered = no_accents.lower()
    # 3) Espacos e underscores viram hifen.
    result = []
    for ch in lowered:
        if ch in (" ", "_"):
            result.append("-")
        elif ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch == "-":
            # 4) Mantem apenas [a-z0-9-]; demais caracteres sao removidos.
            result.append(ch)
        # caractere fora do conjunto permitido: descartado.
    slug = "".join(result)
    # 5) Colapsa hifens repetidos.
    while "--" in slug:
        slug = slug.replace("--", "-")
    # 6) Apara hifens das pontas.
    return slug.strip("-")
