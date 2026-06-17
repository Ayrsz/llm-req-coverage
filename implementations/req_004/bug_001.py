# Fault: off-by-one na fronteira (<= em vez de <).
# IMC exatamente 25 cai em "normal" em vez de "sobrepeso".
def bmi_category(weight: float, height: float) -> str:
    if height <= 0 or weight < 0:
        return "invalido"
    bmi = weight / (height * height)
    if bmi < 18.5:
        return "abaixo"
    if bmi <= 25:
        return "normal"
    if bmi < 30:
        return "sobrepeso"
    return "obesidade"
