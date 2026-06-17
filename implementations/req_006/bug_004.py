# Fault: constante/literal errado no limite de faixa (199 em vez de 255).
# Rejeita octetos válidos no intervalo [200, 255] (ex.: "255.255.255.255").
def is_valid_ipv4(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for octet in parts:
        if octet == "":
            return False
        if not all("0" <= ch <= "9" for ch in octet):
            return False
        if len(octet) > 1 and octet[0] == "0":
            return False
        if int(octet) > 199:
            return False
    return True
