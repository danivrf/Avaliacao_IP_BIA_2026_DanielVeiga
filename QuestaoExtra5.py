# Questao extra – Sudoku
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050

# Referência:
# Professor eu estava tendo muita difilculdade para fazer esse exercicio, entao o código foi baseado no conteúdo do canal "Tech With Tim" no YouTube,
# que apresenta a implementação de um resolvedor de Sudoku utilizando
# o algoritmo de backtracking. Eu apenas realizei algumas modificaçoes como adicionar a biblioteca numpy e deixei ele minimamente jogavel pelo terminal.
#
# Fonte:
# https://www.youtube.com/@TechWithTim
# https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking
#
# Observação:
# Como utilizei uma ideia ja pronta e so adaptei, é totalmente justo eu nao ganhar a nota extra.
#
# O foco aqui é mais a divirsao e conferir se esta rodando corretamente rss.

# Modificações realizadas:
# - Adaptação da estrutura do código
# - Uso da biblioteca NumPy para representar o tabuleiro
# - Criação de versão interativa no terminal


import numpy as np

# Aqui eu defini o tabuleiro inicial do Sudoku.
# O valor 0 representa uma célula vazia que o jogador precisa preencher.
tabuleiro_inicial = np.array([
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
], dtype=int)

# Aqui eu criei uma cópia do tabuleiro inicial.
# Assim eu consigo alterar durante o jogo sem perder o original.
tabuleiro = tabuleiro_inicial.copy()


def mostrar_tabuleiro(tab):
    # Essa função serve apenas para mostrar o tabuleiro de forma organizada no terminal.

    print("\n    1 2 3   4 5 6   7 8 9")
    print("  " + "-" * 25)

    for i in range(9):
        # Aqui eu coloco uma linha separadora a cada 3 linhas
        if i % 3 == 0 and i != 0:
            print("  " + "-" * 25)

        print(f"{i+1} |", end=" ")

        for j in range(9):
            # Aqui separo os blocos 3x3 verticalmente
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            valor = tab[i, j]

            # Se for 0, mostro ponto para indicar célula vazia
            if valor == 0:
                print(".", end=" ")
            else:
                print(valor, end=" ")

        print("|")

    print("  " + "-" * 25)


def eh_valido(tab, numero, posicao):
    # Essa função verifica se um número pode ser colocado
    # em determinada posição do tabuleiro.

    linha, coluna = posicao

    # Verifica a linha
    for j in range(9):
        if tab[linha, j] == numero and j != coluna:
            return False

    # Verifica a coluna
    for i in range(9):
        if tab[i, coluna] == numero and i != linha:
            return False

    # Verifica o bloco 3x3
    bloco_linha = (linha // 3) * 3
    bloco_coluna = (coluna // 3) * 3

    for i in range(bloco_linha, bloco_linha + 3):
        for j in range(bloco_coluna, bloco_coluna + 3):
            if tab[i, j] == numero and (i, j) != posicao:
                return False

    return True


def tabuleiro_completo(tab):
    # Aqui eu verifico se ainda existem zeros no tabuleiro.
    # Se não existir, significa que o jogo foi completado.
    return np.all(tab != 0)


def jogar():
    # Essa é a função principal do jogo.

    print("=== SUDOKU INTERATIVO ===")
    print("Digite: linha coluna numero")
    print("Exemplo: 1 3 5 e não esqueça do espaço entre eles!")
    print("Comandos extras:")
    print("  sair   -> encerra o jogo")
    print("  limpar -> apaga uma jogada sua")
    print()

    while True:
        mostrar_tabuleiro(tabuleiro)

        # Se o tabuleiro estiver completo, o jogador venceu
        if tabuleiro_completo(tabuleiro):
            print("\nParabens! Voce completou o Sudoku.")
            break

        entrada = input("\nSua jogada: ").strip().lower()

        # Comando para sair do jogo
        if entrada == "sair":
            print("Jogo encerrado.")
            break

        # Comando para apagar uma jogada feita pelo usuario
        if entrada == "limpar":
            try:
                linha = int(input("Linha (1-9): ")) - 1
                coluna = int(input("Coluna (1-9): ")) - 1

                # Verifico se a posição é válida
                if not (0 <= linha < 9 and 0 <= coluna < 9):
                    print("Posicao invalida.")
                    continue

                # Não permito apagar valores do tabuleiro original
                if tabuleiro_inicial[linha, coluna] != 0:
                    print("Nao e permitido apagar uma posicao fixa.")
                    continue

                tabuleiro[linha, coluna] = 0
                print("Posicao apagada com sucesso.")

            except ValueError:
                print("Entrada invalida.")

            continue

        partes = entrada.split()

        # Verifico se o formato da entrada está correto
        if len(partes) != 3:
            print("Formato invalido. Digite: linha coluna numero")
            continue

        if not all(parte.isdigit() for parte in partes):
            print("Digite apenas numeros.")
            continue

        linha, coluna, numero = map(int, partes)

        # Ajusto para índice do Python (0 a 8)
        linha -= 1
        coluna -= 1

        # Verifico limites
        if not (0 <= linha < 9 and 0 <= coluna < 9 and 1 <= numero <= 9):
            print("Valores fora do intervalo.")
            continue

        # Não deixo alterar posição fixa do jogo
        if tabuleiro_inicial[linha, coluna] != 0:
            print("Essa posicao nao pode ser alterada.")
            continue

        # Aqui aplico a validação do Sudoku
        if eh_valido(tabuleiro, numero, (linha, coluna)):
            tabuleiro[linha, coluna] = numero
            print("Jogada registrada.")
        else:
            print("Jogada invalida.")


# Aqui eu inicio o jogo chamando a função principal
jogar()