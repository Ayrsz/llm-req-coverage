def is_valid_ipv4(s: str) -> bool:
    # Divide em octetos pelo ponto; exige exatamente 4.
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for octet in parts:
        # Octeto vazio (ponto nas pontas ou consecutivo) é inválido.
        if octet == "":
            return False
        # Apenas dígitos decimais ASCII; rejeita sinais, espaços, letras e
        # dígitos unicode não-ASCII (que quebrariam int()).
        if not all("0" <= ch <= "9" for ch in octet):
            return False
        # Sem zeros à esquerda: comprimento > 1 não pode começar por '0'.
        if len(octet) > 1 and octet[0] == "0":
            return False
        # Valor inteiro deve estar em [0, 255].
        if int(octet) > 255:
            return False
    return True
