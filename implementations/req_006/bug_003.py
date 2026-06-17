# Fault: ramo/retorno trocado (retorna True onde deveria retornar False)
# quando um octeto está fora de faixa. Aceita "1.2.3.999".
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
        if int(octet) > 255:
            return True
    return True
