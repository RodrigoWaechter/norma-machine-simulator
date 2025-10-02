import os
from typing import Dict, List, Tuple 
# ============================
# Registrador
# ============================
class Registrador:
    def __init__(self, nome: str, valor_inicial: int = 0):
        self.nome = nome
        self.valor = valor_inicial

    def inc(self) -> None:
        self.valor += 1

    def dec(self) -> None:
        if self.valor > 0:
            self.valor -= 1

    def zero(self) -> bool:
        return self.valor == 0

    def __repr__(self) -> str:
        return f"{self.nome}={self.valor}"


# ========================================
# Leitura dos "programas" (arquivos .txt)
# ========================================
def ler_programas(pasta: str = "macros") -> Dict[str, Dict[int, str]]:
    programas: Dict[str, Dict[int, str]] = {}
    for arquivo in os.listdir(pasta):
        if not arquivo.endswith(".txt"):
            continue
        caminho = os.path.join(pasta, arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            mapa: Dict[int, str] = {}
            for linha in f:
                linha = linha.strip()
                if not linha or ":" not in linha:
                    continue
                num, texto = linha.split(":", 1)
                mapa[int(num.strip())] = texto.strip()
            programas[arquivo] = mapa
    return programas


# ==========================================
# Parser: quebra uma linha em "blocos" (tokens)
# ==========================================
def quebrar_em_blocos(texto: str) -> List[str]:
    t = texto.strip().split()
    blocos: List[str] = []
    i = 0
    while i < len(t):
        w = t[i]
        if w == "faça":  # normaliza acento
            w = "faca"
        if w == "se" and i + 1 < len(t) and t[i + 1].startswith("zero_"):
            blocos.append(f"se zero_{t[i + 1][5:]}")  # ex: "se zero_a"
            i += 2
        elif w in ("senao", "entao"):
            blocos.append(w); i += 1
        elif w == "va_para":
            if i + 1 < len(t):
                blocos.append(f"va_para {t[i + 1]}"); i += 2
            else:
                blocos.append("va_para"); i += 1
        elif w == "faca":
            if i + 1 < len(t):
                blocos.append(f"faca {t[i + 1]}"); i += 2
            else:
                blocos.append("faca"); i += 1
        else:
            blocos.append(w); i += 1
    return blocos

# ======================================
# Execução: interpreta um arquivo .txt
# ======================================
def executar(
    programas: Dict[str, Dict[int, str]],
    regs: List[Registrador],          
    arquivo: str = "main.txt",
    log: bool = False,  
) -> None:
    prog = programas.get(arquivo)
    if not prog:
        return

    blocos_por_linha = {ln: quebrar_em_blocos(txt) for ln, txt in prog.items()}
    linhas = sorted(blocos_por_linha) 
    if not linhas:
        return

    def prox_linha(ln: int):
        try:
            i = linhas.index(ln)
            return linhas[i + 1]
        except (ValueError, IndexError):
            return None

    atual = linhas[0]  

    while True:
        blocos = list(blocos_por_linha[atual])
        i = 0

        if log:
            print(f"[{arquivo}:{atual}]")

        while i < len(blocos):
            b = blocos[i]
            if b.startswith("faca "):
                b = b.split(" ", 1)[1]

            if b.startswith("se zero_"):
                reg_nome = b.split("zero_", 1)[1]  
                idx = ord(reg_nome) - ord("a")   
                reg = regs[idx]                  
                try:
                    idx_senao = blocos.index("senao", i + 1)
                except ValueError:
                    return
                ini_true = i + 1
                if ini_true < len(blocos) and blocos[ini_true] == "entao":
                    ini_true += 1
                true_part  = blocos[ini_true:idx_senao]   
                false_part = blocos[idx_senao + 1:]     
                escolhido = true_part if reg.zero() else false_part
                blocos = blocos[:i] + escolhido
                continue

            if b.startswith("va_para"):
                partes = b.split()
                if len(partes) != 2 or not partes[1].isdigit():
                    return
                atual = int(partes[1])
                break

            if b.startswith("add_"):
                idx = ord(b[4:]) - ord("a")
                if idx < 0 or idx >= len(regs): return
                regs[idx].inc()
                i += 1
                continue

            if b.startswith("sub_"):
                idx = ord(b[4:]) - ord("a")
                if idx < 0 or idx >= len(regs): return
                regs[idx].dec()
                i += 1
                continue

            if b.startswith("m_"):
                nome_macro = b[2:]
                if not nome_macro.endswith(".txt"):
                    nome_macro += ".txt"
                if nome_macro not in programas:
                    return
                executar(programas, regs, nome_macro, log=log)
                i += 1
                continue

        else:
            proxima = prox_linha(atual)
            if proxima is None:
                return
            atual = proxima
            continue

# ======================================
# Execução: interpreta um arquivo .txt (com logs)
# ======================================
def executar_com_logs(
    programas: Dict[str, Dict[int, str]],
    regs: List[Registrador],
    arquivo: str = "main.txt",
    log_acumulado: List[str] = None
) -> Tuple[List[Registrador], List[str]]:
    
    if log_acumulado is None:
        log_acumulado = []

    prog = programas.get(arquivo)
    if not prog:
        return regs, log_acumulado # Retorno simples em caso de erro

    blocos_por_linha = {ln: quebrar_em_blocos(txt) for ln, txt in prog.items()}
    linhas = sorted(blocos_por_linha)
    if not linhas:
        return regs, log_acumulado

    def prox_linha(ln: int):
        try:
            i = linhas.index(ln)
            return linhas[i + 1]
        except (ValueError, IndexError): return None

    atual = linhas[0]
    # Proteção contra loop infinito removida

    while True:
        # Geração de log de estado mantida
        estado_regs = ", ".join(map(str, regs))
        instrucao = prog.get(atual, "") 
        log_acumulado.append(f"STATE|[{arquivo}:{atual}] -> {instrucao.ljust(50)} | Regs: [{estado_regs}]")

        blocos = list(blocos_por_linha[atual])
        i = 0
        while i < len(blocos):
            b = blocos[i]
            if b.startswith("faca "): b = b.split(" ", 1)[1]
            if b.startswith("se zero_"):
                reg_nome = b.split("zero_", 1)[1]
                idx = ord(reg_nome) - ord("a")
                if not (0 <= idx < len(regs)): return regs, log_acumulado # Retorno simples
                reg = regs[idx]
                try:
                    idx_senao = blocos.index("senao", i + 1)
                    ini_true = i + 1
                    if ini_true < len(blocos) and blocos[ini_true] == "entao": ini_true += 1
                    true_part = blocos[ini_true:idx_senao]
                    false_part = blocos[idx_senao + 1:]
                    blocos = blocos[:i] + (true_part if reg.zero() else false_part)
                    continue
                except ValueError:
                    return regs, log_acumulado # Retorno simples

            if b.startswith("va_para"):
                partes = b.split()
                if len(partes) != 2 or not partes[1].isdigit(): return regs, log_acumulado # Retorno simples
                nova_linha = int(partes[1])
                if nova_linha not in prog: return regs, log_acumulado # Retorno simples
                atual = nova_linha
                break

            # Usando o parse simplificado do 'executar'
            if b.startswith("add_"):
                idx = ord(b[4:]) - ord("a")
                if not (0 <= idx < len(regs)): return regs, log_acumulado # Retorno simples
                regs[idx].inc()
                i += 1; continue

            if b.startswith("sub_"):
                idx = ord(b[4:]) - ord("a")
                if not (0 <= idx < len(regs)): return regs, log_acumulado # Retorno simples
                regs[idx].dec()
                i += 1; continue

            if b.startswith("m_"):
                nome_macro = b[2:] + ".txt" if not b.endswith(".txt") else b[2:]
                if nome_macro not in programas: return regs, log_acumulado # Retorno simples
                # A recursão continua chamando a si mesma para manter o log
                regs, log_acumulado = executar_com_logs(programas, regs, nome_macro, log_acumulado)
                i += 1; continue
            i += 1
        else:
            proxima = prox_linha(atual)
            if proxima is None:
                log_acumulado.append("INFO|--- Fim da Execução ---")
                return regs, log_acumulado
            atual = proxima; continue
    return regs, log_acumulado
