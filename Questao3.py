# Questao 3 – Sistema de Gestao de Estoque com PEPS
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050

# Minha logica foi fazer algo que seguisse a ideia do CRUD, onde o usuario pode, excluir, criar;
# dar opçoes para que o usuario consiga editar mais coisas dentro do etoque. 
# Importei o "datetime" e o "timedelta" do modulo datetime do Python.
# Precisei do datetime para conseguir criar objetos de data reais.
from datetime import datetime, timedelta

# Aqui criei o dicionario principal do sistema, que chamei de "itens".
itens = {}



# FUNCOES AUXILIARES DE LEITURA VALIDADA

def ler_inteiro(prompt, minimo=0):
    # Essa funcao e responsavel por ler um numero inteiro do teclado
    # e garantir que a entrada é valida antes de retornar o valor.

    # Usei um loop "while True" porque quero continuar pedindo a entrada
    # enquanto o usuario errar, sem sair da funcao.

    # Para validar se e um inteiro, usei ".isdigit()" em vez de try/except,
    # lembrei que o senhor falou que poderia dar erros dependendo do codigo e pediu para evitar try/except.
    # O .isdigit() retorna True so se todos os caracteres forem digitos numericos.
    
    # Se o valor for invalido, pergunto se o usuario quer tentar de novo.
    # Se ele disser "N", retorno None — esse None vai ser checado
    # pela funcao que me chamou para saber que a operacao foi cancelada.
    while True:
        entrada = input(prompt).strip()
        if not entrada.isdigit():
            print("Erro: entrada desconhecida! Digite apenas numeros inteiros.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None
            continue
        valor = int(entrada)
        if valor < minimo:
            print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None
            continue
        return valor


def ler_decimal(prompt, minimo=0.0):
    # Essa funcao faz o mesmo papel da ler_inteiro, mas para numeros decimais.
    # A diferenca principal esta na validacao:
    #
    # Primeiro, substituo a virgula por ponto (.replace(",", ".")) para aceitar
    # os dois formatos que o usuario pode digitar — "3,50" ou "3.50".
    #
    # Depois, para checar se e um numero valido, uso um truque:
    # removo UM ponto da string antes de aplicar o .isdigit().
    # Faco isso porque o ponto decimal nao e um digito, entao "3.50".isdigit()
    # retornaria False mesmo sendo um numero valido.
    # Com o .replace(".", "", 1) eu removo apenas a primeira ocorrencia do ponto,
    # ai o que sobra ("350") passa no .isdigit() normalmente.
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        if not entrada.replace(".", "", 1).isdigit():
            print("Erro: entrada desconhecida! Digite apenas numeros (ex: 3.50).")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None
            continue
        valor = float(entrada)
        if valor < minimo:
            print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None
            continue
        return valor


def ler_data(prompt):
    # Essa foi a funcao mais trabalhosa de validar porque precisei checar
    # o formato DD/MM/AAAA inteiramente na mao, sem usar try/except.
    #
    # A estrategia que adotei foi validar em camadas, da mais simples
    # para a mais especifica, parando com uma mensagem de erro
    # assim que encontrar qualquer problema:
    #
    #   1. Verifico se a string tem exatamente 10 caracteres
    #      e se as barras estao nas posicoes certas (indice 2 e 5).
    #   2. Separo os trechos de dia, mes e ano usando fatiamento de string
    #      (sei exatamente onde cada parte fica no formato DD/MM/AAAA).
    #   3. Verifico se cada trecho e composto so de digitos com .isdigit().
    #   4. Converto para inteiro e verifico se mes esta entre 1 e 12.
    #   5. Verifico se dia esta entre 1 e 31.
    #
    # No final, crio o objeto datetime com os valores validados.
    # Retorno uma tupla com dois valores:
    #   - o objeto datetime (para poder fazer calculos com datas depois)
    #   - a string formatada (para exibir de forma legivel no relatorio)
    # Se o usuario cancelar, retorno (None, None) para sinalizar isso.
    while True:
        entrada = input(prompt).strip()

        # Camada 1: verifico o tamanho e a posicao das barras
        if len(entrada) != 10 or entrada[2] != "/" or entrada[5] != "/":
            print("Erro: formato invalido! Use DD/MM/AAAA (ex: 20/04/2026).")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None, None
            continue

        # Camada 2: separo os trechos por fatiamento de string
        # entrada[0:2] pega os caracteres das posicoes 0 e 1 → dia
        # entrada[3:5] pega os caracteres das posicoes 3 e 4 → mes
        # entrada[6:10] pega os caracteres das posicoes 6 a 9 → ano
        dia_str = entrada[0:2]
        mes_str = entrada[3:5]
        ano_str = entrada[6:10]

        # Camada 3: verifico se cada trecho e so digito
        if not dia_str.isdigit() or not mes_str.isdigit() or not ano_str.isdigit():
            print("Erro: a data deve conter apenas numeros e barras.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None, None
            continue

        dia = int(dia_str)
        mes = int(mes_str)
        ano = int(ano_str)

        # Camada 4: verifico o intervalo do mes
        if not (1 <= mes <= 12):
            print("Erro: mes invalido! O mes deve estar entre 01 e 12.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None, None
            continue

        # Camada 5: verifico o intervalo do dia
        if not (1 <= dia <= 31):
            print("Erro: dia invalido! O dia deve estar entre 01 e 31.")
            continuar = input("Deseja tentar novamente? (S/N): ").upper()
            if continuar != "S":
                return None, None
            continue

        # Com tudo validado, crio o objeto datetime e ja formato a string
        # para exibicao usando strftime com o padrao DD/MM/AAAA.
        dt = datetime(ano, mes, dia)
        return dt, dt.strftime("%d/%m/%Y")

# 1. FUNCAO PARA CADASTRAR ITENS

def cadastrar_itens():
    # Primeiro pergunto quantos itens o usuario quer cadastrar de uma vez.
    # Uso minimo=1 porque nao faz sentido cadastrar zero itens.
    qtd_itens = ler_inteiro("Quantos itens deseja cadastrar? ", minimo=1)
    if qtd_itens is None:
        # Se ler_inteiro retornou None, o usuario cancelou, entao saio da funcao.
        print("Cadastro cancelado.")
        return

    # Uso for em vez de while porque ja sei exatamente quantas vezes
    # o loop vai rodar — o numero que o usuario informou.
    for i in range(qtd_itens):
        print(f"\nCadastro do item {i+1}")

        # Leio o nome do item e imediatamente verifico se ele ja existe
        # no dicionario para evitar duplicatas.
        nome = input("Descreva o item: ").strip()
        if nome in itens:
            print("Erro: esse item ja esta cadastrado.")
            continue  # pulo para a proxima iteracao do for

        unidade = input(
            "Qual a unidade de medida dele (ex: unidade, caixa, resma): ").strip()

        # Permito saldo inicial zero porque o item pode ser cadastrado
        # antes de chegar fisicamente ao estoque.
        saldo_inicial = ler_inteiro("Saldo inicial em estoque: ", minimo=0)
        if saldo_inicial is None:
            print("Cadastro do item cancelado.")
            continue

        # O valor do saldo inicial vai compor o primeiro lote PEPS do item.
        # E essencial registra-lo porque o PEPS precisa saber o custo
        # de cada lote para calcular o valor total do estoque corretamente.
        valor_inicial = ler_decimal(
            "Valor unitario do saldo inicial: R$ ", minimo=0.0)
        if valor_inicial is None:
            print("Cadastro do item cancelado.")
            continue

        # O consumo medio diario e o lead time sao os dois dados que
        # eu uso para calcular o ponto de ressuprimento.
        # Formula: PR = consumo_diario x lead_time
        consumo_diario = ler_decimal(
            "Qual o consumo medio diario desse item: ", minimo=0.0)
        if consumo_diario is None:
            print("Cadastro do item cancelado.")
            continue

        lead_time = ler_inteiro(
            "Qual o tempo de reposicao em dias: ", minimo=1)
        if lead_time is None:
            print("Cadastro do item cancelado.")
            continue

        # Registro a data em que o item foi cadastrado no sistema.
        # Essa data vai ser o ponto de partida para o calculo do
        # prazo limite de compra no relatorio: vou somar a ela
        # os dias que o estoque ainda aguenta antes de atingir o PR.
        dt_cadastro, data_cadastro_fmt = ler_data(
            "Data de cadastro do item (DD/MM/AAAA): ")
        if dt_cadastro is None:
            print("Cadastro do item cancelado.")
            continue

        # Monto o dicionario do item com todos os campos necessarios
        # e insiro ele no dicionario principal "itens" usando o nome como chave.
        #
        # Sobre os campos:
        # - "saldo" e o saldo atual, que vai mudar conforme as movimentacoes.
        # - "saldo_inicial" e uma referencia fixa para comparar no relatorio
        #   se o estoque cresceu, diminuiu ou ficou estavel.
        # - "lotes" e a fila PEPS: uma lista de tuplas (quantidade, valor).
        #   O primeiro elemento da lista e sempre o lote mais antigo,
        #   que sera consumido primeiro nas saidas.
        # - "total_saidas" acumula todas as saidas para calcular o giro.
        # - "movimentacoes" guarda o historico cronologico de entradas e saidas.
        # - "dt_cadastro" e o objeto datetime (para calculos com timedelta).
        # - "data_cadastro" e a string formatada (para exibir ao usuario).
        itens[nome] = {
            "unidade":          unidade,
            "saldo":            saldo_inicial,
            "saldo_inicial":    saldo_inicial,
            "consumo_diario":   consumo_diario,
            "lead_time":        lead_time,
            "lotes":            [(saldo_inicial, valor_inicial)],
            "total_saidas":     0,
            "movimentacoes":    [],
            "dt_cadastro":      dt_cadastro,
            "data_cadastro":    data_cadastro_fmt,
        }

        print(f"Item cadastrado com sucesso em {data_cadastro_fmt}!")



# 2. FUNCAO PARA EXCLUIR ITEM

def excluir_item():
    print("\n--- Excluir item ---")

    # Verifico de imediato se ha algo para excluir.
    # Nao faz sentido pedir o nome de um item se o dicionario esta vazio.
    if not itens:
        print("Nenhum item cadastrado para excluir.")
        return

    nome = input("Digite o nome do item que deseja excluir: ").strip()

    # Verifico se o nome digitado existe antes de tentar excluir,
    # para evitar um erro de chave inexistente.
    if nome not in itens:
        print("Erro: item nao encontrado.")
        return

    # Peco uma confirmacao explicita para evitar exclusoes acidentais.
    confirmacao = input(
        f"Tem certeza que deseja excluir '{nome}'? (S/N): ").upper()

    if confirmacao == "S":
        # "del" remove a chave e todo o dicionario associado a ela de uma vez.
        del itens[nome]
        print("Item excluido com sucesso!")
    else:
        print("Exclusao cancelada.")

# 3. FUNCAO PARA VER ESTOQUE

def ver_estoque():
    print("\n=====================")
    print("ESTOQUE ATUAL")
    print("=====================\n")
    if not itens:
        print("Nenhum item cadastrado ainda.")
        return

    # Uso .items() para iterar sobre o dicionario e ter acesso
    # simultaneamente ao nome (chave) e aos dados (valor) de cada item.
    for nome, item in itens.items():
        print(f"Item: {nome}")
        print(f"Unidade: {item['unidade']}")
        print(f"Data de cadastro: {item['data_cadastro']}")
        print(f"Saldo atual: {item['saldo']}")
        print(f"Saldo inicial: {item['saldo_inicial']}")
        print(f"Consumo medio diario: {item['consumo_diario']}")
        print(f"Lead time: {item['lead_time']} dias")
        print(f"Total de saidas: {item['total_saidas']}")

        # Mostro cada lote separadamente para que o usuario enxergue
        # a fila PEPS como ela esta: o primeiro lote listado sera
        # o primeiro a ser consumido na proxima saida.
        print("Lotes em estoque:")
        for qtd_lote, valor_lote in item["lotes"]:
            print(f"  - {qtd_lote} unidades a R$ {valor_lote:.2f}")

        # Mostro o historico so se houver movimentacoes registradas,
        # para nao poluir a tela de itens recem-cadastrados.
        if item["movimentacoes"]:
            print("Historico de movimentacoes:")
            for mov in item["movimentacoes"]:
                print(f"  [{mov['data']}] {mov['tipo']} | "
                      f"Qtd: {mov['quantidade']} | "
                      f"Valor unit.: R$ {mov['valor']:.2f}")

        print("-" * 40)



# 4. FUNCAO PARA REGISTRAR MOVIMENTACOES

def registrar_movimentacoes():
    if not itens:
        print("Erro: nao ha itens cadastrados para movimentar.")
        return

    qtd_movimentacao = ler_inteiro(
        "\nQuantas movimentacoes deseja registrar? ", minimo=1)
    if qtd_movimentacao is None:
        print("Registro cancelado.")
        return

    for i in range(qtd_movimentacao):
        print(f"\nMovimentacao {i+1}")

        # Aqui uso while True em vez de chamar ler_inteiro porque
        # nao quero oferecer cancelamento para o nome do item —
        # o usuario precisa obrigatoriamente informar um item valido
        # para que a movimentacao possa ser registrada.
        while True:
            nome = input("Item: ").strip()
            if nome not in itens:
                print("Erro: item nao encontrado! Digite um item cadastrado.")
            else:
                break

        # Mesma logica para o tipo: so aceito ENTRADA ou SAIDA,
        # e fico no loop ate receber uma dessas duas opcoes.
        while True:
            tipo = input("Tipo (ENTRADA/SAIDA): ").upper()
            if tipo not in ["ENTRADA", "SAIDA"]:
                print("Erro: tipo invalido! Digite ENTRADA ou SAIDA.")
            else:
                break

        quantidade = ler_inteiro("Quantidade: ", minimo=1)
        if quantidade is None:
            print("Movimentacao cancelada.")
            continue

        valor = ler_decimal("Valor unitario: R$ ", minimo=0.0)
        if valor is None:
            print("Movimentacao cancelada.")
            continue

        dt_mov, data_formatada = ler_data(
            "Data da movimentacao (DD/MM/AAAA): ")
        if dt_mov is None:
            print("Movimentacao cancelada.")
            continue

        # Crio uma referencia direta ao dicionario do item para nao precisar
        # escrever itens[nome] toda hora nas linhas abaixo.
        item = itens[nome]

      
        # LOGICA DE ENTRADA
       
        if tipo == "ENTRADA":
            # Numa entrada, aumento o saldo e adiciono o novo lote
            # ao FINAL da lista. No criterio PEPS, entradas mais recentes
            # ficam no final e serao consumidas por ultimo — o que chegou
            # primeiro sai primeiro.
            item["saldo"] += quantidade
            item["lotes"].append((quantidade, valor))
            item["movimentacoes"].append({
                "tipo":       "ENTRADA",
                "quantidade": quantidade,
                "valor":      valor,
                "data":       data_formatada,
                "dt":         dt_mov
            })
            print(f"Entrada registrada com sucesso em {data_formatada}!")

      
        # LOGICA DE SAIDA COM O CRITERIO PEPS
       
        elif tipo == "SAIDA":
            # Antes de qualquer coisa, verifico se ha saldo suficiente.
            # Se nao houver, cancelo a operacao sem alterar nada.
            if quantidade > item["saldo"]:
                print("Erro: saldo insuficiente! Movimentacao nao registrada.")
                continue

            # Atualizo o saldo geral e acumulo no total de saidas,
            # que usarei depois para identificar o item com maior giro.
            item["saldo"] -= quantidade
            item["total_saidas"] += quantidade

            # Aqui implemento o PEPS de verdade.
            # A ideia e percorrer os lotes do mais antigo para o mais novo
            # e ir "consumindo" cada um ate a quantidade solicitada ser atendida.
            #
            # "restante" controla quantas unidades ainda precisam ser retiradas.
            # "novos_lotes" vai acumular os lotes que sobrarem apos a saida.
            restante = quantidade
            novos_lotes = []

            for qtd_lote, valor_lote in item["lotes"]:
                if restante == 0:
                    # Ja consumi tudo que precisava.
                    # Copio os lotes restantes sem alterar nada.
                    novos_lotes.append((qtd_lote, valor_lote))
                    continue

                if qtd_lote <= restante:
                    # Este lote inteiro cabe no que ainda preciso retirar.
                    # Consumo ele por completo e subtraio do restante.
                    # Nao adiciono em novos_lotes porque ele foi totalmente usado.
                    restante -= qtd_lote
                else:
                    # Este lote tem mais do que o restante que preciso.
                    # Retiro so o necessario e guardo o que sobrou do lote.
                    novos_lotes.append((qtd_lote - restante, valor_lote))
                    restante = 0

            # Substituo a lista de lotes original pela nova lista,
            # que ja reflete o consumo PEPS que acabei de calcular.
            item["lotes"] = novos_lotes
            item["movimentacoes"].append({
                "tipo":       "SAIDA",
                "quantidade": quantidade,
                "valor":      valor,
                "data":       data_formatada,
                "dt":         dt_mov
            })
            print(f"Saida registrada com sucesso em {data_formatada}!")

# 5. FUNCAO PARA GERAR RELATORIO FINAL

def gerar_relatorio():
    print("\n=== RELATORIO FINAL ===\n")

    if not itens:
        print("Nenhum item cadastrado.")
        return

    # Inicializo com string vazia e zero para comparar durante o loop.
    # Ao final, essa variavel vai conter o item com mais saidas totais.
    maior_giro = ("", 0)

    for nome, item in itens.items():

        # CALCULO DO VALOR TOTAL EM ESTOQUE PELO CRITERIO PEPS
        # Percorro os lotes que sobraram apos todas as saidas e multiplico
        # a quantidade de cada lote pelo seu valor unitario.
        # Como o PEPS ja eliminou os lotes mais antigos nas saidas anteriores,
        # o que resta aqui sao exatamente os lotes mais recentes — e e isso
        # que o criterio PEPS determina para a avaliacao do estoque final.
        valor_total = 0
        for qtd_lote, valor_lote in item["lotes"]:
            valor_total += qtd_lote * valor_lote

        # PONTO DE RESSUPRIMENTO E ALERTA DE COMPRA
        # O ponto de ressuprimento (PR) e o nivel de estoque a partir do qual
        # preciso fazer um novo pedido de compra para nao ficar sem estoque
        # durante o tempo que o fornecedor leva para entregar (lead time).
        # Formula: PR = consumo_diario x lead_time
        ponto_ressuprimento = item["consumo_diario"] * item["lead_time"]

        # Se o saldo atual estiver abaixo do PR, o sistema avisa que precisa comprar.
        precisa_comprar = item["saldo"] < ponto_ressuprimento

        # CALCULO DO PRAZO LIMITE DE COMPRA
        # Quero saber em qual data o estoque vai atingir o ponto de
        # ressuprimento, para que o gestor saiba ate quando pode esperar
        # para fazer o pedido sem correr risco de ruptura.
        #
        # Calculo quantos dias o saldo atual aguenta acima do PR:
        #   dias_restantes = (saldo_atual - PR) / consumo_diario
        #
        # Depois somo esses dias a data de cadastro usando timedelta,
        # que e exatamente para isso — fazer aritmetica com datas.
        #
        # Se o consumo diario for zero, nao posso dividir por ele,
        # entao exibo uma mensagem indicando que o prazo nao se aplica.
        if item["consumo_diario"] > 0:
            dias_restantes = (
                item["saldo"] - ponto_ressuprimento) / item["consumo_diario"]

            # Se o resultado for negativo, o estoque ja passou do ponto critico,
            # entao uso zero para indicar que o prazo ja estourou.
            if dias_restantes < 0:
                dias_restantes = 0

            dt_prazo = item["dt_cadastro"] + timedelta(days=dias_restantes)
            prazo_compra = dt_prazo.strftime("%d/%m/%Y")
        else:
            prazo_compra = "Sem consumo registrado"

        # COMPARACAO COM O SALDO INICIAL
        # Comparo o saldo atual com o saldo que o item tinha quando foi
        # cadastrado. Foi por isso que guardei o "saldo_inicial" como
        # um campo separado — ele nao muda com as movimentacoes,
        # servindo como ponto de referencia fixo para essa comparacao.
        if item["saldo"] > item["saldo_inicial"]:
            status = "Cresceu"
        elif item["saldo"] < item["saldo_inicial"]:
            status = "Diminuiu"
        else:
            status = "Estavel"

        # Atualizo o maior giro se este item tiver mais saidas do que
        # o atual lider. Ao sair do loop, "maior_giro" contera
        # o nome e a quantidade do item mais movimentado.
        if item["total_saidas"] > maior_giro[1]:
            maior_giro = (nome, item["total_saidas"])

        # EXIBICAO DO RELATORIO DE CADA ITEM
     
        print(f"Item: {nome}")
        print(f"Data de cadastro        : {item['data_cadastro']}")
        print(f"Saldo atual             : {item['saldo']} {item['unidade']}")
        print(f"Valor total (PEPS)      : R$ {valor_total:.2f}")
        print(
            f"Ponto de ressuprimento  : {ponto_ressuprimento:.2f} {item['unidade']}")
        print(f"Prazo limite de compra  : {prazo_compra}")

        if precisa_comprar:
            print(
                "ATENCAO: Estoque abaixo do ponto de ressuprimento! Compra imediata necessaria.")
        else:
            print("Estoque acima do ponto de ressuprimento.")

        print(f"Situacao do estoque     : {status}")

        if item["movimentacoes"]:
            print("Movimentacoes registradas:")
            for mov in item["movimentacoes"]:
                print(f"  [{mov['data']}] {mov['tipo']} | "
                      f"Qtd: {mov['quantidade']} | "
                      f"Valor unit.: R$ {mov['valor']:.2f}")

        print("-" * 40)

    # Apos percorrer todos os itens, exibo o destaque de maior giro.
    # Esse dado ajuda a identificar quais itens tem mais rotatividade
    # e merecem mais atencao na gestao do estoque.
    print(f"\nItem com maior giro: {maior_giro[0]} ({maior_giro[1]} saidas)")


# O menu e o ponto de entrada do programa e funciona como um hub central
# que direciona o usuario para cada funcionalidade, ja havia feito isso em outos codigos e achei que ficaria bom usar nesse.
#
# Escolhi usar "while True" porque quero manter o programa rodando
# indefinidamente ate o usuario decidir sair — nao faz sentido o sistema
# encerrar sozinho apos uma unica operacao.

while True:
    print("\n================ MENU ================")
    print("1 - Ver estoque")
    print("2 - Cadastrar itens")
    print("3 - Registrar movimentacoes")
    print("4 - Gerar relatorio final")
    print("5 - Excluir item")
    print("6 - Sair")
    print("======================================")

    opcao = input("Escolha uma opcao: ").strip()

    if opcao == "1":
        ver_estoque()
    elif opcao == "2":
        cadastrar_itens()
    elif opcao == "3":
        registrar_movimentacoes()
    elif opcao == "4":
        gerar_relatorio()
    elif opcao == "5":
        excluir_item()
    elif opcao == "6":
        print("Encerrando o sistema...")
        break  # unico ponto de saida do loop — encerra o programa
    else:
        print("Erro: opcao invalida.")