# Fault: operador errado (double soma a si mesmo de forma errada: usa + em vez de *).
# Aqui troca a multiplicação por adição de 2.


def apply_commands(start: int, commands: list) -> int:
    counter = start
    for command in commands:
        if command == "inc":
            counter += 1
        elif command == "dec":
            if counter > 0:
                counter -= 1
        elif command == "double":
            counter += 2
        elif command == "reset":
            counter = 0
    return counter
