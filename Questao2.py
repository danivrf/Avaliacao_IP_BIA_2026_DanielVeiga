# Questao 2 – Surto de Colera – Limpeza e Analise Epidemiologica
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050


import pandas as pd

print("Iniciando analise epidemiologica...\n")

# 1. CARREGAMENTO DOS DADOS

# Aqui eu carrego o arquivo CSV diretamente do link fornecido na questao.
# exatamente como na questão 1.

df = pd.read_csv("https://re-dir.prezenzaa.com.br/iUy7IQ")

# Padronizei os nomes das colunas para evitar problemas com espacos,
# letras maiusculas ou inconsistencias de escrita.
# O .str.strip() remove espacos antes e depois do texto.
# O .str.lower() deixa todos os nomes em minusculo.
df.columns = df.columns.str.strip().str.lower()
print("========================")
print("VISUALIZACÃO INICIAL")
print("========================\n")
# O metodo .head() mostra as primeiras linhas do dataset.
# Eu mantive essa exibicao para demonstrar que fiz uma exploracao inicial
# da base antes de comecar a limpeza.
print(df.head())
print("\n")

print("=====================")
print("INFO DO DATAFRAME")
print("=====================\n")
# O metodo .info() mostra:
# - quantidade de linhas e colunas
# - nome e tipo de dado de cada coluna
# - quantidade de valores nao nulos
# Eu usei isso para entender melhor a estrutura da base.
df.info()
print("\n")

print("=========================")
print("VALORES NULOS POR COLUNA")
print("=========================\n")

# O isnull() identifica valores ausentes.
# O sum() soma quantos valores nulos existem em cada coluna.
# Isso ajuda a decidir quais colunas precisam de tratamento.
print(df.isnull().sum())
print("\n")

# Criei uma copia do DataFrame original para fazer a limpeza
# sem perder a base original carregada.
df_limpo = df.copy()

# 2. LIMPEZA DOS DADOS

# Estrategia adotada:
# - tratei cada coluna de forma apropriada
# - removi apenas valores impossiveis ou inconsistentes
# - mantive dados potencialmente relevantes sempre que possivel
# - evitei perda desnecessaria de informacao

# COLUNAS DE TEXTO

# Converto para string e removo espacos para padronizar os dados textuais.
# Isso ajuda a evitar problemas de comparacao e agrupamento.
df_limpo["id_cd"] = df_limpo["id_cd"].astype(str).str.strip()
df_limpo["cd_pai"] = df_limpo["cd_pai"].astype(str).str.strip()

# Na coluna regiao, alem de remover espacos,
# eu uso .str.title() para padronizar o formato do texto.
# Assim, por exemplo, "norte", "NORTE" e " Norte " tendem a ficar iguais.
df_limpo["regiao"] = df_limpo["regiao"].astype(str).str.strip().str.title()


# COLUNAS NUMERICAS

# O pd.to_numeric() converte os valores das colunas para numeros.
# O errors="coerce" faz com que valores invalidos sejam transformados em NaN,
# o que permite tratar esses problemas depois.
df_limpo["populacao_atendida"] = pd.to_numeric(
    df_limpo["populacao_atendida"], errors="coerce")

df_limpo["casos_suspeitos"] = pd.to_numeric(
    df_limpo["casos_suspeitos"], errors="coerce")

# Guardo a quantidade inicial de linhas para depois comparar
# quanto restou apos a limpeza.
linhas_antes_limpeza = len(df_limpo)

# Para casos_suspeitos, tratei valores nulos como 0.
# Minha justificativa é que, em uma primeira analise epidemiologica,
# a ausência de registro de casos suspeitos pode ser interpretada
# como ausência de ocorrencia informada naquele ponto de coleta.

df_limpo["casos_suspeitos"] = df_limpo["casos_suspeitos"].fillna(0)

# Para populacao_atendida, usei a mediana para preencher valores ausentes.
# Escolhi a mediana porque ela tende a sofrer menos influencia
# de valores muito extremos do que a media.
mediana_populacao = df_limpo["populacao_atendida"].median()
df_limpo["populacao_atendida"] = df_limpo["populacao_atendida"].fillna(
    mediana_populacao)

# Aqui eu removo apenas registros impossiveis ou inconsistentes:
# - populacao_atendida precisa ser maior que 0
# - casos_suspeitos nao pode ser negativo
# - casos_suspeitos nao pode ser maior que a populacao atendida
df_limpo = df_limpo[df_limpo["populacao_atendida"] > 0]
df_limpo = df_limpo[df_limpo["casos_suspeitos"] >= 0]
df_limpo = df_limpo[df_limpo["casos_suspeitos"]
                    <= df_limpo["populacao_atendida"]]


# COLUNA DE DATA

# O pd.to_datetime() converte a coluna para tipo data.
# O errors="coerce" evita erro caso alguma data esteja invalida,
# convertendo valores problematicos para NaT.
df_limpo["data_coleta"] = pd.to_datetime(
    df_limpo["data_coleta"], errors="coerce")

# Aqui eu conto quantas datas invalidas existem apos a conversao.
# Nao removi automaticamente esses registros porque,
# como a analise principal da questao e por regiao,
# o restante da informacao ainda pode ser util.
qtd_datas_invalidas = df_limpo["data_coleta"].isnull().sum()

print("=====================")
print("VERIFICAÇÃO DE DATAS")
print("=====================\n")
print(f"Quantidade de datas inválidas: {qtd_datas_invalidas}")
print("\n")

print("Linhas com datas inválidas:")
print(df_limpo[df_limpo["data_coleta"].isnull()])
print("\n")


# DUPLICATAS

# Removo duplicatas considerando id_cd e data_coleta juntos.
# Escolhi esse criterio porque registros repetidos para o mesmo centro
# na mesma data podem indicar duplicacao indevida.
df_limpo = df_limpo.drop_duplicates(subset=["id_cd", "data_coleta"])

linhas_depois_limpeza = len(df_limpo)

print("=====================")
print("RESUMO DA LIMPEZA")
print("=====================\n")
print(f"Linhas antes da limpeza: {linhas_antes_limpeza}")
print(f"Linhas depois da limpeza: {linhas_depois_limpeza}")
print(f"Linhas removidas: {linhas_antes_limpeza - linhas_depois_limpeza}")
print("\n")

print("=====================")
print("DADOS APOS LIMPEZA")
print("=====================\n")
print(df_limpo.head())
print("\n")

print("===========================")
print("VALORES NULOS APÓS LIMPEZA")
print("===========================\n")
print(df_limpo.isnull().sum())
print("\n")

# 3. CALCULO DA TAXA DE INCIDENCIA

# A taxa de incidencia foi calculada como:
# casos_suspeitos / populacao_atendida * 1000
# Multipliquei por 1000 para representar a incidencia por mil habitantes,
# o que facilita a comparacao entre centros com populacoes diferentes.
df_limpo["taxa_incidencia"] = (
    df_limpo["casos_suspeitos"] / df_limpo["populacao_atendida"] * 1000).round(4)

print("===================================")
print("ESTATÍSTICAS DA TAXA DE INCIDÊNCIA")
print("===================================\n")

# O .describe() mostra resumo estatistico da taxa calculada.
print(df_limpo["taxa_incidencia"].describe())
print("\n")

print("Todas as taxas ordenadas:")
print(df_limpo["taxa_incidencia"].sort_values().values.round(2))
print("\n")

print(f"Menor taxa: {df_limpo['taxa_incidencia'].min()}")
print(f"Maior taxa: {df_limpo['taxa_incidencia'].max()}")
print("\n")


# 4. CLASSIFICACAO EPIDEMIOLOGICA COM apply E row


# Aqui eu percebi que o enunciado pede que a taxa seja calculada
# como casos_suspeitos / populacao_atendida dentro da propria funcao.
# Por isso mudei a funcao para receber a linha inteira (row),
# igual ao padrao que usei na questao 1 com classificar_imc.
# Assim a funcao acessa as duas colunas diretamente e calcula
# a taxa internamente antes de classificar.
#
# Os limites foram definidos a partir da distribuicao dos dados:
# - valores abaixo de 0.30 concentram a maior parte dos registros
#   e representam o comportamento basal esperado: normal
# - valores entre 0.30 e 0.99 indicam aumento acima do padrao,
#   mas ainda sem caracterizar uma situacao grave: atencao
# - valores entre 1.00 e 2.99 representam aumento mais expressivo
#   da incidencia: alerta
# - valores iguais ou superiores a 3.00 representam niveis extremos: critico
def classificar_alerta(row):
    # Calculo a taxa aqui dentro, como o enunciado sugere:
    # casos_suspeitos / populacao_atendida
    taxa = row["casos_suspeitos"] / row["populacao_atendida"] * 1000

    if taxa < 0.30:
        return "normal"
    elif taxa < 1.00:
        return "atencao"
    elif taxa < 3.00:
        return "alerta"
    else:
        return "critico"


# O axis=1 faz o pandas percorrer linha por linha,
df_limpo["nivel_alerta"] = df_limpo.apply(classificar_alerta, axis=1)

print("==================================")
print("DISTRIBUIÇÃO DOS NÍVEIS DE ALERTA")
print("==================================\n")

# O value_counts() conta quantas vezes cada classificacao aparece.
print(df_limpo["nivel_alerta"].value_counts())
print("\n")


# 5. CLASSIFICACAO DOS CDs

# Aqui eu monto uma exibicao mais organizada da classificacao dos CDs,
# mostrando as principais colunas da analise.
print("=====================")
print("CLASSIFICAÇÃO DOS CDs")
print("=====================\n")

colunas_exibir = [
    "id_cd",
    "regiao",
    "populacao_atendida",
    "casos_suspeitos",
    "taxa_incidencia",
    "nivel_alerta"
]

print(df_limpo[colunas_exibir].head(20).to_string(index=False))
print(f"\n... ({len(df_limpo)} registros no total)\n")

# 6. RESUMO POR NIVEL DE ALERTA

# Aqui eu crio um resumo agrupando os CDs por nivel_alerta.
# Com isso, consigo ver:
# - quantos registros existem em cada nivel
# - a taxa media daquele grupo
# - a taxa maxima observada
print("==========================")
print("RESUMO POR NIVEL DE ALERTA")
print("==========================\n")

resumo_alerta = (
    df_limpo.groupby("nivel_alerta")
    .agg(
        qtd_registros=("nivel_alerta", "count"),
        taxa_media=("taxa_incidencia", "mean"),
        taxa_max=("taxa_incidencia", "max")
    )
    .round(4)
    .reset_index()
)

print(resumo_alerta.to_string(index=False))
print("\n")

# 7. RELATORIO EPIDEMIOLOGICO POR REGIAO

print("===================================")
print("RELATÓRIO EPIDEMIOLOGICO POR REGIÃO")
print("===================================\n")

# O groupby("regiao") agrupa os dados por regiao.
# O .agg() permite calcular varias medidas ao mesmo tempo:
# - taxa media de incidencia
# - total de casos suspeitos
# - numero de centros de distribuicao
relatorio = df_limpo.groupby("regiao").agg(
    taxa_media_incidencia=("taxa_incidencia", "mean"),
    total_casos=("casos_suspeitos", "sum"),
    numero_cds=("id_cd", "count")
).reset_index()

# Arredondo a taxa media para 2 casas decimais
# para deixar a exibicao mais organizada.
relatorio["taxa_media_incidencia"] = relatorio["taxa_media_incidencia"].round(
    2)

# Aqui eu monto a distribuicao dos niveis de alerta por regiao.
# O pd.crosstab() conta quantos registros de cada nivel_alerta
# existem dentro de cada regiao.
distribuicao_alertas = pd.crosstab(
    df_limpo["regiao"], df_limpo["nivel_alerta"]).reset_index()

# Junto o relatorio principal com a distribuicao dos alertas.
relatorio_final = pd.merge(
    relatorio,
    distribuicao_alertas,
    on="regiao",
    how="left"
)

print(relatorio_final.to_string(index=False))
print("\n")

# 8. RELATORIO RESUMIDO COM MAIOR NIVEL DE ALERTA POR REGIAO

# Aqui eu defini uma ordem de gravidade para os niveis de alerta.
# Quanto maior o numero, mais grave e o nivel.
ordem_alerta = {
    "normal": 1,
    "atencao": 2,
    "alerta": 3,
    "critico": 4
}

# Converto os niveis de alerta para valores numericos de gravidade.
df_limpo["nivel_gravidade"] = df_limpo["nivel_alerta"].map(ordem_alerta)

# Para cada regiao, pego o maior nivel de gravidade encontrado.
# Isso garante que, se existir pelo menos um caso critico,
# a regiao inteira sera considerada critica no resumo.
nivel_regiao = (df_limpo.groupby("regiao")[
                "nivel_gravidade"].max().reset_index())

# Dicionario inverso para converter o numero de volta para o nome do alerta.
ordem_inversa = {
    1: "normal",
    2: "atencao",
    3: "alerta",
    4: "critico"
}

# Converto o nivel numerico de volta para texto.
nivel_regiao["nivel_alerta_final"] = nivel_regiao["nivel_gravidade"].map(
    ordem_inversa)

# Seleciono apenas as colunas finais.
nivel_regiao = nivel_regiao[["regiao", "nivel_alerta_final"]]

print("=== NIVEL DE ALERTA POR REGIAO (MAIOR GRAVIDADE) ===\n")
print(nivel_regiao.to_string(index=False))
print("\n")

# 9. CONCLUSOES
print("=====================")
print("CONCLUSÕES")
print("=====================\n")
# Aqui eu identifico a regiao com maior total de casos suspeitos.
regiao_mais_casos = relatorio_final.loc[relatorio_final["total_casos"].idxmax(
), "regiao"]

# Aqui eu identifico a regiao com maior taxa media de incidencia.
regiao_maior_taxa = relatorio_final.loc[relatorio_final["taxa_media_incidencia"].idxmax(
), "regiao"]

# Se a coluna critico existir, eu tambem identifico a regiao
# com maior quantidade de centros criticos.
if "critico" in relatorio_final.columns:
    regiao_mais_criticos = relatorio_final.loc[
        relatorio_final["critico"].idxmax(),
        "regiao"
    ]
    print(f"Regiao com maior numero de CDs criticos: {regiao_mais_criticos}")

print(f"Regiao com maior total de casos suspeitos: {regiao_mais_casos}")
print(f"Regiao com maior taxa media de incidencia: {regiao_maior_taxa}")
print(f"Taxa media geral do dataset: {df_limpo['taxa_incidencia'].mean():.4f}")

print("\nAnálise finalizada com sucesso.")
print("=================================")
