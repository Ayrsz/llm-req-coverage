# Fault: operador aritmético errado (height * 2 em vez de height ao quadrado).
# IMC calculado incorretamente, deslocando classificacoes.
def bmi_category(weight: float, height: float) -> str:
    if height <= 0 or weight < 0:
        return "invalido"
    bmi = weight / (height * 2)
    if bmi < 18.5:
        return "abaixo"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "sobrepeso"
    return "obesidade"
