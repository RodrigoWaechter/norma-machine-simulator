# Simulador de Máquina Norma

Este projeto é uma implementação em Python de um simulador para a Máquina Norma, um modelo teórico de computação que opera com um conjunto de registradores de valores inteiros não negativos. O simulador conta com uma interface gráfica para facilitar a interação, edição de código e visualização do processo de computação.

## Funcionalidades

- **Interface Gráfica**: Uma interface de usuário construída com a biblioteca Tkinter, que permite a interação visual com o simulador.
- **Configuração de Registradores**: Permite definir o número de registradores que serão utilizados (de 1 a 26, de 'a' a 'z') e seus valores iniciais.
- **Editor de Código Integrado**: A interface possui um editor de texto para criar e modificar os programas da Máquina Norma, que são salvos em arquivos .txt.
- **Suporte a Macros**: O sistema permite que um programa chame outros programas (macros) armazenados em arquivos .txt dentro da pasta `macros`.
- **Visualização da Execução**: A interface exibe um log detalhado de cada passo da computação, mostrando a instrução executada e o estado de todos os registradores naquele momento.
- **Execução via Terminal**: Inclui um script auxiliar para testes rápidos da lógica do simulador diretamente no terminal.

## Estrutura do Projeto

O projeto é organizado nos seguintes arquivos e pastas:

- `app.py`: Contém todo o código da interface gráfica (GUI). É o arquivo principal para interagir com o simulador.
- `norma.py`: É o núcleo do simulador. Implementa a lógica da Máquina Norma, incluindo a manipulação de registradores, a interpretação de instruções e a execução dos programas.
- `exec.py`: Um script simples usado para executar a lógica do `norma.py` via terminal, útil para testes e depuração sem a camada gráfica.
- `macros/`: Uma pasta que deve conter todos os programas e macros em formato .txt. O simulador carrega os arquivos desta pasta para a memória.

## Como Executar o Projeto

### Pré-requisitos

- Python 3 instalado no seu sistema.
O projeto utiliza apenas bibliotecas padrão do Python, como `os` e `tkinter`, não sendo necessária a instalação de pacotes externos.

### Executando a Interface Gráfica (Recomendado)

Para usar o simulador com a interface visual, execute o seguinte comando no seu terminal, na pasta raiz do projeto:

```
python app.py
```
Executando via Terminal (Para Testes)
Para realizar um teste rápido da lógica principal, você pode usar o script exec.py. Ele executará o main.txt e imprimirá o estado final dos registradores no console.

```
python exec.py
```

## Como Usar o Simulador
1. **Configuração:**
- **Nº de Registradores:** Defina quantos registradores a máquina usará (ex: 3 para a, b, c).
- **Valores Iniciais:** Insira os valores iniciais para cada registrador. Por padrão, eles começam em 0.

2. **Editor de Código:**
- O seletor de "Arquivo" permite que você escolha qual programa da pasta macros/ deseja visualizar ou editar.
- O arquivo main.txt é o ponto de entrada principal para o botão "Executar Programa (main.txt)".
- Escreva seu código no formato número: instrução. Por exemplo:
```
1: sub_b
2: sub_a
3: se zero_a sub_a senao m_exemplomacro
```

 3. **Execução:**
- **Executar Programa (main.txt):** Executa o código que está salvo no arquivo main.txt.
- **Executar Arquivo Aberto:** Executa o código do arquivo que está atualmente selecionado e aberto no editor.
- **Limpar:** Limpa a tela de log e o estado final dos registradores.

4. **Resultados:**
- **Computação Completa:** Mostra cada passo da execução, linha por linha.
- **Estado Final dos Registradores:** Exibe os valores de todos os registradores após o término do programa.

# Documentação
[MaquinaNorma.pdf](https://github.com/user-attachments/files/22661976/MaquinaNorma.pdf)

# Autores
- Rodrigo Waechter
- Gabriel Witt
- Gustavo Mohr
- Ana Werle
