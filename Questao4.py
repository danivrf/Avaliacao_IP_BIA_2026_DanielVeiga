# Questao 4 – Primesweeper
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050



# Nesta questao, o objetivo e simular a logica base do jogo Primesweeper.

# 1. FUNCAO PARA AVALIAR A CELULA

def avaliar_celula(n):
    # Esta funcao recebe um numero inteiro n
    # e retorna duas informacoes:
    # - o status da celula
    # - o payload correspondente

    # Caso especial: 0 e 1
    # Esses valores nao sao primos nem compostos,
    # entao o enunciado manda tratar como INDEF.
    if n == 0 or n == 1:
        return "INDEF", None

    # Aqui eu percorro todos os inteiros de 2 ate n-1.
    # A ideia e procurar o primeiro divisor exato de n.
    # Se eu encontrar um divisor, significa que o numero e composto.
    for divisor in range(2, n):

        # O operador % calcula o resto da divisao.
        # Se n % divisor == 0, significa que a divisao foi exata,
        # entao divisor é um divisor de n.
        if n % divisor == 0:

            # Nesse caso, retorno SAFE e o divisor encontrado como payload.
            # o primeiro divisor encontrado.
            return "SAFE", divisor

    # Se o laco terminou e nenhum divisor foi encontrado,
    # significa que o numero e primo.
    # Nesse caso, o status e MINA e o payload e None.
    return "MINA", None

# Aqui eu executo automaticamente os casos de teste.
print("=======================")
print("TESTE AUTOMATICO")
print("=======================\n")

casos_teste = [0, 1, 2, 9, 17, 49, 100]

# Aqui eu percorro a lista de casos de teste.
# Para cada numero, chamo a funcao avaliar_celula()
# e imprimo o resultado no formato que foi pedido na questão.
for n in casos_teste:
    status, payload = avaliar_celula(n)
    print(f"CELULA {n} :: STATUS={status} :: PAYLOAD={payload}")

# Esta parte nao era obrigatoria no enunciado,
# mas eu adicionei como recurso extra, assim como na questao anterior, usei um while, onde o usuario pode testar outros numeros
# mais para brincar mesmo, e para fins de curiosidade rss.

print("\n=== MODO INTERATIVO ===")

while True:
    entrada = input("\nDigite um numero (ou 'sair'): ")

    # Se o usuario digitar "sair", o programa encerra.
    if entrada.lower() == "sair":
        print("Encerrando...")
        break

    # Aqui eu valido se a entrada contem apenas digitos.
    # Usei isdigit() para evitar try/except novamente.
    # com inteiros nao negativos (n >= 0).
    #
    # Se a entrada nao for composta apenas por digitos,
    # o programa exibe uma mensagem de erro e volta ao inicio do loop.
    if not entrada.isdigit():
        print("Erro: digite um numero inteiro nao negativo.")
        continue

    # Depois da validacao, converto a entrada para inteiro.
    n = int(entrada)

    # Chamo a funcao principal para avaliar o numero digitado.
    status, payload = avaliar_celula(n)

    # Exibo o resultado no mesmo formato exigido pelo enunciado.
    print(f"CELULA {n} :: STATUS={status} :: PAYLOAD={payload}")
