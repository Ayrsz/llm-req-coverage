# Fault: operador errado na contagem de octetos (< em vez de !=).
# Não rejeita strings com mais de 4 octetos (ex.: "1.2.3.4.5").
def is_valid_ipv4(s: str) -> bool:
    parts = s.split(".")
    if len(parts) < 4:
        return False
    for octet in parts:
        if octet == "":
            return False
        if not all("0" <= ch <= "9" for ch in octet):
            return False
        if len(octet) > 1 and octet[0] == "0":
            return False
        if int(octet) > 255:
            return False
    return True
