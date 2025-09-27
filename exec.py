from norma import *

if __name__ == "__main__":
    regs = [Registrador("a", 2), Registrador("b", 3)]
    programas = ler_programas("macros")
    executar(programas, regs, "main.txt", log = True)
    print(regs)
 