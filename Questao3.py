# Questao 3 – Sistema de Gestao de Estoque com PEPS
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050

# Minha logica foi fazer algo que seguisse a ideia do CRUD.
# Nessa versao integrei pandas, numpy e datetime para deixar o codigo menor e mais eficiente
# que eu fazia antes com for e variaveis acumuladoras.
#
# - datetime / timedelta : criacao de datas e calculo do prazo de compra
# - numpy  : calculo vetorizado do valor total dos lotes (sem loop manual, pois notei que o codigo iria ficar muito maior com esses loops)
# - pandas : exibicao tabular do historico, relatorio e estatisticas gerais

from datetime import datetime, timedelta
import numpy as np
import pandas as pd

itens = {}

def ler_inteiro(prompt, minimo=0):
# Lê um número inteiro com validação, garantindo que seja numérico
# e maior ou igual ao mínimo, repetindo até ser válido ou o usuário cancelar.
    while True:
        entrada = input(prompt).strip()
        if not entrada.isdigit():
            print("Erro: entrada desconhecida! Digite apenas numeros inteiros.")
            # Se o usuario nao quiser tentar de novo, retorno None
            # para sinalizar o cancelamento a quem me chamou.
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None
            continue
        valor = int(entrada)
        if valor < minimo:
            print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None
            continue
        return valor


def ler_decimal(prompt, minimo=0.0):
# Lê um número decimal com validação, garantindo formato correto
# e valor mínimo, repetindo até ser válido ou o usuário sair.
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        if not entrada.replace(".", "", 1).isdigit():
            print("Erro: entrada desconhecida! Digite apenas numeros (ex: 3.50).")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None
            continue
        valor = float(entrada)
        if valor < minimo:
            print(f"Erro: o valor deve ser maior ou igual a {minimo}.")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None
            continue
        return valor


def ler_data(prompt):
# Valida DD/MM/AAAA em camadas.
    while True:
        entrada = input(prompt).strip()
        # A ideia geral é um while True que fica repetindo até receber uma data válida ou o usuário cancelar. 
        # O len(entrada) checa se a string tem exatamente 10 caracteres e se as barras estão nas posições certas.
        if len(entrada) != 10 or entrada[2] != "/" or entrada[5] != "/":
            print("Erro: formato invalido! Use DD/MM/AAAA (ex: 20/04/2026).")
            # Se o usuário não quiser tentar novamente, eu encerro a função
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None, None
            continue
        # Aqui eu separo dia, mês e ano usando slicing
        dia_str, mes_str, ano_str = entrada[:2], entrada[3:5], entrada[6:]
        # Aqui eu verifico se cada parte é realmente numérica
        if not dia_str.isdigit() or not mes_str.isdigit() or not ano_str.isdigit():
            print("Erro: a data deve conter apenas numeros e barras.")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None, None
            continue
        # Converto as strings para inteiro
        dia, mes, ano = int(dia_str), int(mes_str), int(ano_str)
        # Valido o mês (1 a 12)
        if not (1 <= mes <= 12):
            print("Erro: mes invalido! O mes deve estar entre 01 e 12.")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None, None
            continue
        # Valido o dia (1 a 31)
        if not (1 <= dia <= 31):
            print("Erro: dia invalido! O dia deve estar entre 01 e 31.")
            if input("Deseja tentar novamente? (S/N): ").upper() != "S":
                return None, None
            continue
        # Aqui eu crio o objeto datetime com os valores validados
        dt = datetime(ano, mes, dia)
        # Retorno a data em dois formatos:
        return dt, dt.strftime("%d/%m/%Y")

def cadastrar_itens():
# Função responsável por cadastrar novos itens no sistema.
# Valida cada entrada (inteiro, decimal e data) e, se tudo estiver correto,
# armazena o item no dicionário com suas informações iniciais.
# Caso o usuário cancele em algum ponto, o cadastro é interrompido.
    qtd_itens = ler_inteiro("Quantos itens deseja cadastrar? ", minimo=1)
    if qtd_itens is None:
        print("Cadastro cancelado.")
        return

    for i in range(qtd_itens):
        print(f"\nCadastro do item {i+1}")

        nome = input("Descreva o item: ").strip()
        if nome in itens:
            print("Erro: esse item ja esta cadastrado.")
            continue

        unidade        = input("Unidade de medida (ex: unidade, caixa, resma): ").strip()
        saldo_inicial  = ler_inteiro("Saldo inicial em estoque: ", minimo=0)
        #Aqui eu fui atras de tentar deixar o codigo mais fluido. 
        # Se ler_inteiro retornou None, o significa usuario cancelou —
        # nao faz sentido continuar o cadastro sem esse dado.
        if saldo_inicial is None: print("Cadastro cancelado."); continue

        valor_inicial  = ler_decimal("Valor unitario do saldo inicial: R$ ", minimo=0.0)
        if valor_inicial is None: print("Cadastro cancelado."); continue

        consumo_diario = ler_decimal("Consumo medio diario: ", minimo=0.0)
        if consumo_diario is None: print("Cadastro cancelado."); continue

        lead_time      = ler_inteiro("Tempo de reposicao (dias): ", minimo=1)
        if lead_time is None: print("Cadastro cancelado."); continue

        dt_cadastro, data_fmt = ler_data("Data de cadastro (DD/MM/AAAA): ")
        if dt_cadastro is None: print("Cadastro cancelado."); continue

        # So crio o lote inicial se houver quantidade real.
        # Um lote (0, valor) nunca seria consumido e distorceria
        # o calculo de valor total feito pelo numpy no relatorio.
        itens[nome] = {
            "unidade":        unidade,
            "saldo":          saldo_inicial,
            "saldo_inicial":  saldo_inicial,
            "consumo_diario": consumo_diario,
            "lead_time":      lead_time,
            "lotes":          [(saldo_inicial, valor_inicial)] if saldo_inicial > 0 else [],
            "total_saidas":   0,
            "movimentacoes":  [],
            "dt_cadastro":    dt_cadastro,
            "data_cadastro":  data_fmt,
        }
        print(f"Item '{nome}' cadastrado com sucesso em {data_fmt}!")

def excluir_item():
# Função que remove um item do sistema.
# Verifica se o item existe e pede confirmação antes de excluir.
# Caso o usuário não confirme ou o item não exista, a operação é cancelada.
    print("\n--- Excluir item ---")
    if not itens:
        print("Nenhum item cadastrado para excluir.")
        return
    nome = input("Nome do item a excluir: ").strip()
    if nome not in itens:
        print("Erro: item nao encontrado.")
        return
    if input(f"Confirmar exclusao de '{nome}'? (S/N): ").upper() == "S":
        del itens[nome]
        print("Item excluido com sucesso!")
    else:
        print("Exclusao cancelada.")

# 3. FUNCAO PARA VER ESTOQUE

def ver_estoque():
    print("\n=== ESTOQUE ATUAL ===\n")
    if not itens:
        print("Nenhum item cadastrado ainda.")
        return

    for nome, item in itens.items():
        print(f"Item: {nome} | Unidade: {item['unidade']} | "
              f"Cadastro: {item['data_cadastro']} | "
              f"Saldo: {item['saldo']} | Saidas: {item['total_saidas']}")

        # Antes eu tinha um for separado para printar cada lote manualmente.
        # Agora converto a lista de lotes direto em DataFrame e exibo como tabela.
        # pd.DataFrame(lista, columns=[...]) cria a tabela ja com os nomes certos.
        if item["lotes"]:
            df_lotes = pd.DataFrame(item["lotes"], columns=["Qtd", "Valor Unit. (R$)"])
            print(df_lotes.to_string(index=False))

        # Antes eu tinha outro for para printar cada movimentacao linha por linha.
        # Agora converto a lista de dicionarios em DataFrame e seleciono
        # apenas as colunas que quero mostrar, renomeando para ficar mais legivel.
        if item["movimentacoes"]:
            df_mov = pd.DataFrame(item["movimentacoes"])[["data","tipo","quantidade","valor"]]
            df_mov.columns = ["Data", "Tipo", "Qtd", "Valor Unit. (R$)"]
            print(df_mov.to_string(index=False))

        print("-" * 40)

def registrar_movimentacoes():
# Função responsável por registrar entradas e saídas no estoque.
# Valida item, tipo, quantidade, valor e data; aplica a lógica PEPS nas saídas
# e registra todas as movimentações no histórico do item.
    if not itens:
        print("Erro: nao ha itens cadastrados para movimentar.")
        return

    qtd_mov = ler_inteiro("\nQuantas movimentacoes deseja registrar? ", minimo=1)
    if qtd_mov is None:
        print("Registro cancelado.")
        return

    for i in range(qtd_mov):
        print(f"\nMovimentacao {i+1}")

        # Uso while True aqui porque o usuario precisa obrigatoriamente
        # informar um item valido, nao tem opcao de cancelamento aqui.
        while True:
            nome = input("Item: ").strip()
            if nome not in itens: print("Erro: item nao encontrado!")
            else: break

        while True:
            tipo = input("Tipo (ENTRADA/SAIDA): ").upper()
            if tipo not in ["ENTRADA", "SAIDA"]: print("Erro: digite ENTRADA ou SAIDA.")
            else: break

        quantidade = ler_inteiro("Quantidade: ", minimo=1)
        # Se ler_inteiro retornou None, o usuario cancelou a entrada do dado.
        # Uso "continue" para pular essa movimentacao inteira e ir para a proxima,
        # evitando registrar uma movimentacao com dados incompletos.
        if quantidade is None: print("Movimentacao cancelada."); continue

        valor = ler_decimal("Valor unitario: R$ ", minimo=0.0)
        # Mesma logica: se o usuario cancelou o valor, nao registro nada
        # e pulo para a proxima movimentacao com continue.
        if valor is None: print("Movimentacao cancelada."); continue

        dt_mov, data_fmt = ler_data("Data da movimentacao (DD/MM/AAAA): ")
        # Mesma logica para a data: sem ela nao consigo registrar a movimentacao.
        if dt_mov is None: print("Movimentacao cancelada."); continue

        item = itens[nome]

        if tipo == "ENTRADA":
            item["saldo"]  += quantidade
            item["lotes"].append((quantidade, valor))

        elif tipo == "SAIDA":
            if quantidade > item["saldo"]:
                print("Erro: saldo insuficiente! Movimentacao nao registrada.")
                continue
            item["saldo"]        -= quantidade
            item["total_saidas"] += quantidade

            # Logica PEPS: consumo os lotes mais antigos primeiro.
            # "restante" controla quanto ainda precisa ser retirado.
            # "novos_lotes" acumula o que sobrar apos a saida.
            # Inicializo as duas variaveis na mesma linha para ficar mais enxuto.
            restante, novos_lotes = quantidade, []
            for qtd_lote, valor_lote in item["lotes"]:
                if restante == 0:
                    novos_lotes.append((qtd_lote, valor_lote))
                elif qtd_lote <= restante:
                    restante -= qtd_lote
                else:
                    novos_lotes.append((qtd_lote - restante, valor_lote))
                    restante = 0
            item["lotes"] = novos_lotes

        # Registro a movimentacao independente do tipo,
        # porque o bloco acima ja tratou ENTRADA e SAIDA separadamente.
        item["movimentacoes"].append({
            "tipo": tipo, "quantidade": quantidade,
            "valor": valor, "data": data_fmt, "dt": dt_mov
        })
        print(f"{tipo} registrada com sucesso em {data_fmt}!")

def gerar_relatorio():
# Função que gera o relatório final do estoque.
# Calcula valor total pelo PEPS, ponto de ressuprimento, prazo de compra,
# situação de cada item e monta tudo em uma tabela com Pandas.
# No final, também mostra algumas estatísticas gerais usando NumPy.
    print("\n=== RELATORIO FINAL ===\n")
    if not itens:
        print("Nenhum item cadastrado.")
        return

    # Vou acumular os dados de cada item nessa lista
    # para no final montar um DataFrame com todos de uma vez.
    resumo = []

    for nome, item in itens.items():

        # VALOR TOTAL PEPS COM NUMPY
        # np.array(item["lotes"]) transforma a lista de tuplas em uma matriz:
        # coluna 0 = quantidades, coluna 1 = valores unitarios
        # arr[:, 0] pega toda a coluna de quantidades.
        # arr[:, 1] pega toda a coluna de valores.
        # Multiplico as duas colunas elemento a elemento e somo tudo com np.sum.
        if item["lotes"]:
            arr         = np.array(item["lotes"])
            valor_total = float(np.sum(arr[:, 0] * arr[:, 1]))
        else:
            valor_total = 0.0

        # PONTO DE RESSUPRIMENTO E PRAZO DE COMPRA
        # PR = consumo_diario x lead_time
        pr              = item["consumo_diario"] * item["lead_time"]
        precisa_comprar = item["saldo"] < pr

        # Calculo quantos dias o saldo ainda aguenta acima do PR.
        # max(..., 0) evita resultado negativo quando o saldo ja passou do PR.
        # timedelta soma esses dias a data de cadastro para ter a data exata.
        if item["consumo_diario"] > 0:
            dias  = max((item["saldo"] - pr) / item["consumo_diario"], 0)
            prazo = (item["dt_cadastro"] + timedelta(days=dias)).strftime("%d/%m/%Y")
        else:
            prazo = "Sem consumo"

        # COMPARACAO SALDO INICIAL x ATUAL
        # "diff" guarda a diferenca entre os dois para decidir o status.
        diff   = item["saldo"] - item["saldo_inicial"]
        status = "Cresceu" if diff > 0 else "Diminuiu" if diff < 0 else "Estavel"

        resumo.append({
            "Item":         nome,
            "Saldo Ini.":   item["saldo_inicial"],
            "Saldo Atual":  item["saldo"],
            "Valor (R$)":   round(valor_total, 2),
            "Pt. Ressup.":  round(pr, 2),
            "Prazo Compra": prazo,
            "Comprar?":     "SIM" if precisa_comprar else "nao",
            "Situacao":     status,
            "Tot. Saidas":  item["total_saidas"],
        })

    # RELATORIO TABULAR COM PANDAS
    # Converto a lista de dicionarios em DataFrame.
    # Antes eu tinha um bloco de prints para cada campo de cada item —
    # agora um unico to_string() exibe tudo em formato de tabela.
    df = pd.DataFrame(resumo)
    print(df.to_string(index=False))

    # ESTATISTICAS GERAIS COM NUMPY
    # Converto as colunas que preciso em arrays numpy para calcular
    # as metricas sem precisar de loops adicionais.
    # np.sum   → soma todos os valores do array
    # np.mean  → calcula a media
    # np.argmax → retorna o indice do maior valor (uso para pegar o nome)
    # np.argmin → retorna o indice do menor valor
    valores = np.array([r["Valor (R$)"]   for r in resumo])
    saldos = np.array([r["Saldo Atual"]  for r in resumo])
    saidas = np.array([r["Tot. Saidas"]  for r in resumo])
    nomes = [r["Item"] for r in resumo]

    print(f"\nValor total do estoque: R$ {np.sum(valores):.2f}")
    print(f"Saldo medio por item: {np.mean(saldos):.2f}")
    print(f"Item com maior giro: {nomes[int(np.argmax(saidas))]} "
          f"({int(np.max(saidas))} saidas)")
    print(f"Item com menor saldo: {nomes[int(np.argmin(saldos))]}")



# E por ultimo o while feito para o menu principal do projeto, que chama todas as funçoes
# e faz o codigo girar.

# while True mantem o programa rodando ate o usuario escolher sair.
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

    if   opcao == "1": ver_estoque()
    elif opcao == "2": cadastrar_itens()
    elif opcao == "3": registrar_movimentacoes()
    elif opcao == "4": gerar_relatorio()
    elif opcao == "5": excluir_item()
    elif opcao == "6": print("Encerrando o sistema..."); break
    else: print("Erro: opcao invalida.")
