from norma import *

if __name__ == "__main__":
    regs = [Registrador("a", 2), Registrador("b", 3), Registrador("c", 0), Registrador("d", 0), Registrador("e", 0)]
    programas = ler_programas("macros")
    executar(programas, regs, "main.txt", log = True)
    print(regs)
 