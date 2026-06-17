# Fault: guarda ausente (não trata weight < 0 na condição de invalidez).
# Peso negativo com altura positiva produz IMC negativo -> "abaixo".
def bmi_category(weight: float, height: float) -> str:
    if height <= 0:
        return "invalido"
    bmi = weight / (height * height)
    if bmi < 18.5:
        return "abaixo"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "sobrepeso"
    return "obesidade"
