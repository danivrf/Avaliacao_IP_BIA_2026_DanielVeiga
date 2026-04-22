# Questao 1 – Classificacao de IMC por faixa etaria
# Disciplina: Introducao a Programacao – BIA/UFG
# Professor: Leonardo Antonio Alves
# Aluno: Daniel Veiga Rodrigues de Faria
# Matricula: 202603050

# Importei a biblioteca pandas porque ela facilita a leitura e a manipulacao
# de dados em formato de tabela, como arquivos CSV.
# Com ela eu consigo carregar o arquivo, criar colunas novas, agrupar dados,
# calcular estatisticas e aplicar funcoes nas linhas do DataFrame.

import pandas as pd

# Aqui eu carrego o arquivo CSV diretamente do link fornecido.
# O pandas transforma esse arquivo em um DataFrame,
# que funciona como uma tabela dentro do Python.
df = pd.read_csv("https://re-dir.prezenzaa.com.br/KL4UDa")

print("========================")
print("VISUALIZACÃO INICIAL")
print("========================\n")

# O metodo .head() mostra as primeiras 5 linhas da base.
# Eu usei isso para fazer uma primeira visualizaçao dos dados presentes dentro do arquivo
print(df.head())
print("\n")

# O metodo .tail() mostra as ultimas 5 linhas do DataFrame.
# Eu mantive isso para verificar se os dados continuam consistentes no final.
print(df.tail())
print("\n")

# Como a base nao possui a coluna idade pronta,
# eu calculei a idade com base na coluna data_nascimento.

# O metodo pd.to_datetime() converte a coluna para o tipo data.
# O errors="coerce" evita erro caso alguma data esteja invalida.
# Se isso acontecer, o valor sera convertido para NaT,
# que e equivalente ao None ou ao NaN apresentado nas literaturas.
df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce")

# Aqui eu pego a data atual do sistema para usar como referencia.
hoje = pd.Timestamp.today()

# Primeiro eu calculo a idade de forma aproximada,
# subtraindo o ano atual pelo ano de nascimento.
df["idade"] = hoje.year - df["data_nascimento"].dt.year

# Depois eu ajusto essa idade para os casos em que a pessoa
# ainda nao fez aniversario no ano atual.
# O .dt permite acessar partes da data, como ano, mes e dia.
df["idade"] -= (
    (hoje.month < df["data_nascimento"].dt.month) |
    (
        (hoje.month == df["data_nascimento"].dt.month) &
        (hoje.day < df["data_nascimento"].dt.day)
    )
)

print("========================")
print("VISUALIZACÃO DAS IDADES")
print("========================\n")

# Aqui eu mostro uma amostra da data de nascimento e da idade calculada
# para conferir se o calculo foi feito corretamente.
print(df[["data_nascimento", "idade"]].head())
print("\n")

print("========================")
print("INFORMAÇÕES DO DATAFRAME")
print("========================\n")

# O metodo .info() mostra um resumo tecnico do DataFrame:
# nome das colunas, tipo dos dados, quantidade de valores nao nulos
# e quantidade total de linhas.
df.info()
print("\n")

print("==============================================")
print("ESTATÍSTICAS DESCRITIVAS DAS COLUNAS NUMÉRICAS")
print("==============================================\n")

# O metodo .describe() gera estatisticas descritivas das colunas numericas.
# O round(..., 2) foi usado apenas para deixar a exibicao mais organizada.
print(df.describe().round(2))
print("\n")

# a) CALCULO DO IMC

# O IMC foi calculado pela formula: peso / altura^2
# Como o pandas permite operacoes diretas entre colunas,
# eu aplico essa formula em toda a base de uma vez.
# O .round(2) serve para deixar os valores com 2 casas decimais.
df["imc"] = (df["peso_kg"] / (df["altura_m"] ** 2)).round(2)


# b) FAIXA ETARIA E CLASSIFICACAO DO IMC COM apply


# Criei esta funcao para transformar a idade numerica
# em uma classificacao de faixa etaria.
def faixa_etaria(idade):
    if idade < 12:
        return "crianca"
    elif idade <= 17:
        return "adolescente"
    elif idade <= 59:
        return "adulto"
    else:
        return "idoso"


# O metodo .apply() aplica a funcao em todos os valores da coluna idade.
# Assim eu gero uma nova coluna chamada faixa_etaria.
df["faixa_etaria"] = df["idade"].apply(faixa_etaria)

# Aqui eu percebi que classificar o IMC depende tanto da idade quanto do imc
# ao mesmo tempo, entao precisei usar apply com axis=1 para percorrer
# linha por linha e acessar as duas colunas juntas.
# Por isso a funcao recebe "row", que representa uma linha inteira do DataFrame,
# e eu acesso cada coluna pelo nome dentro dela. Pois dependia de mais de uma coluna ao mesmo tempo.

# Para criancas e adolescentes, a OMS recomenda o uso de curvas
# de IMC por idade (escore Z). Mas optei por usar os valores aproximados, para encaixar melhor
# com a logica que defini para o codigo.


def classificar_imc(row):
    idade = row["idade"]
    imc = row["imc"]

    # criancas
    if idade < 12:
        if imc < 14.0:
            return "magreza_acentuada"
        elif imc < 16.0:
            return "magreza"
        elif imc < 25.0:
            return "eutrofico"
        elif imc < 28.0:
            return "sobrepeso"
        else:
            return "obesidade"

    # adolescentes
    elif idade <= 17:
        if imc < 16.0:
            return "magreza_acentuada"
        elif imc < 18.0:
            return "magreza"
        elif imc < 25.0:
            return "eutrofico"
        elif imc < 30.0:
            return "sobrepeso"
        else:
            return "obesidade"

    # adultos
    elif idade <= 59:
        if imc < 18.5:
            return "abaixo_peso"
        elif imc < 25.0:
            return "peso_normal"
        elif imc < 30.0:
            return "sobrepeso"
        elif imc < 35.0:
            return "obesidade_grau_1"
        elif imc < 40.0:
            return "obesidade_grau_2"
        else:
            return "obesidade_grau_3"

    # idosos
    else:
        if imc < 22.0:
            return "abaixo_peso"
        elif imc < 27.0:
            return "eutrofico"
        elif imc < 30.0:
            return "sobrepeso"
        else:
            return "obesidade"


# passando cada linha como um objeto Series para a funcao.
df["classificacao_imc"] = df.apply(classificar_imc, axis=1)

# Aqui eu defini quais classificacoes serao consideradas como risco.
RISCO = {
    "magreza_acentuada",
    "magreza",
    "abaixo_peso",
    "sobrepeso",
    "obesidade",
    "obesidade_grau_1",
    "obesidade_grau_2",
    "obesidade_grau_3"
}

# c-i) CONTAGEM E PERCENTUAL POR CLASSIFICACAO DENTRO DE CADA FAIXA ETARIA


def analise_contagem_percentual(df):
    print("\nContagem e Percentual\n")

    # O groupby() agrupa os dados por faixa_etaria e classificacao_imc.
    # O .size() conta quantas pessoas existem em cada grupo.
    # Usei reset_index para transformar o resultado em um DataFrame normal,
    # o que facilita as operacoes seguintes.
    contagem = (df.groupby(
        ["faixa_etaria", "classificacao_imc"]).size().reset_index(name="contagem"))

    # Para calcular o percentual dentro de cada faixa etaria,
    # primeiro preciso saber o total de pessoas em cada faixa.
    total_faixa = (df.groupby("faixa_etaria").size().reset_index(name="total"))

    # Aqui eu uno as duas tabelas pelo campo faixa_etaria usando merge,
    # para que cada linha de contagem tenha o total da sua faixa ao lado.
    # O merge e mais explicito e funciona em todas as versoes recentes do pandas pelas literaturas.
    contagem = contagem.merge(total_faixa, on="faixa_etaria")

    # Agora consigo calcular o percentual dividindo a contagem pelo total.
    contagem["percentual_%"] = (
        contagem["contagem"] / contagem["total"] * 100).round(2)

    # Removo a coluna total porque ela so era necessaria para o calculo.
    contagem = contagem.drop(columns="total")

    print("Contagem e percentual por faixa etaria:")
    print(contagem.to_string(index=False))

# c-ii) IMC MEDIO, MEDIANO E DESVIO-PADRAO POR FAIXA ETARIA E SEXO


def analise_estatisticas(df):
    print("\nEstatÍsticas do IMC\n")

    # O groupby() agrupa por faixa_etaria e sexo.
    # O .agg() permite aplicar varias funcoes estatisticas ao mesmo tempo,
    # que no caso foram a media, mediana e desvio padrao.
    estatisticas = df.groupby(["faixa_etaria", "sexo"])["imc"].agg(
        media="mean",
        mediana="median",
        desvio_padrao="std"
    ).round(2)

    print(estatisticas)

# c-iii) TABELA COM GRUPOS DE MAIOR PROPORCAO DE RISCO (faixa etaria x sexo)


def analise_risco(df):
    print("\nAnÁlise de Risco\n")

    # O .isin() verifica se a classificacao_imc pertence ao conjunto RISCO.
    # O resultado e uma coluna booleana: True para risco e False para nao risco.
    df["risco"] = df["classificacao_imc"].isin(RISCO)

    # Como True vale 1 e False vale 0,
    # a media dessa coluna representa a proporcao de risco no grupo.
    # Aqui eu tambem uso reset_index e sort_values para deixar a tabela
    # organizada do maior para o menor risco.
    risco_grupo = (
        df.groupby(["faixa_etaria", "sexo"])["risco"]
          .mean()
          .round(2)
          .reset_index(name="proporcao_risco")
          .sort_values("proporcao_risco", ascending=False)
    )

    print("Proporcao de risco por grupo (faixa etaria x sexo):")
    print(risco_grupo.to_string(index=False))

    print("\nGrupo com maior proporcao de risco:")
    print(risco_grupo.head(1).to_string(index=False))


# RESULTADOS INICIAIS
print("========================")
print("RESULTADOS INICIAIS")
print("========================\n")

# Aqui eu mostro as primeiras linhas ja com as novas colunas criadas
# para verificar se os calculos foram aplicados corretamente.
print(df.head())
print("\n")

print("=============================")
print("DISTRIBUIÇÃO DE CLASSIFICAÇÃO")
print("=============================\n")

# O value_counts() conta quantas vezes cada classificacao aparece.
print(df["classificacao_imc"].value_counts())
print("\n")

print("Tabela cruzada:")

# O pd.crosstab() gera uma tabela cruzada entre faixa_etaria
# e classificacao_imc.
print(pd.crosstab(df["faixa_etaria"], df["classificacao_imc"]))
print("\n")

# Aqui eu filtro apenas as pessoas que estao em risco,
# usando o mesmo criterio definido anteriormente.
df_risco = df[df["classificacao_imc"].isin(RISCO)]

print("==============================")
print("QUANTIDADE DE PESSOAS EM RISCO")
print("==============================\n")

# O len() retorna o numero de linhas do DataFrame filtrado.
print(len(df_risco))
print("\n")

print("=================================")
print("PESSOAS EM RISCO POR FAIXA ETARIA:")
print("=================================\n")


# O value_counts() mostra quantas pessoas em risco existem em cada faixa etaria.
print(df_risco["faixa_etaria"].value_counts())
print("\n")

print("===================================================")
print("IMC medio das pessoas em risco (separado por tipo):")
print("===================================================\n")

# Aqui eu separo os casos de magreza acentuada
df_magreza_acentuada = df[df["classificacao_imc"] == "magreza_acentuada"]
# Aqui eu separo os casos de magreza
df_magreza = df[df["classificacao_imc"] == "magreza"]

# Aqui eu separo os casos de obesidade e seus graus
df_obesidade = df[df["classificacao_imc"].isin([
    "obesidade",
    "obesidade_grau_1",
    "obesidade_grau_2",
    "obesidade_grau_3"
])]

# Aqui eu separo os casos de sobrepeso
df_sobrepeso = df[df["classificacao_imc"] == "sobrepeso"]

# Aqui eu separo os casos de abaixo do peso
df_abaixo_peso = df[df["classificacao_imc"] == "abaixo_peso"]

# Antes de calcular a media, eu verifico se existe pelo menos um caso
# para evitar erro ou resultado vazio.
if len(df_magreza_acentuada) > 0:
    print("IMC medio (magreza_acentuada):", round(
        df_magreza_acentuada["imc"].mean(), 2))
else:
    print("IMC medio (magreza_acentuada): nao ha dados")

if len(df_magreza) > 0:
    print("IMC medio (magreza_acentuada):", round(df_magreza["imc"].mean(), 2))
else:
    print("IMC medio (magreza_acentuada): nao ha dados")

if len(df_obesidade) > 0:
    print("IMC medio (obesidade):", round(df_obesidade["imc"].mean(), 2))
else:
    print("IMC medio (obesidade): nao ha dados")

if len(df_sobrepeso) > 0:
    print("IMC medio (sobrepeso):", round(df_sobrepeso["imc"].mean(), 2))
else:
    print("IMC medio (sobrepeso): nao ha dados")

if len(df_abaixo_peso) > 0:
    print("IMC medio (abaixo_peso):", round(df_abaixo_peso["imc"].mean(), 2))
else:
    print("IMC medio (abaixo_peso): nao ha dados")

print("\n")

print("============================")
print("IMC medio por faixa etaria:")
print("============================\n")
# Aqui eu percorro as faixas etarias e calculo a media do IMC em cada uma.
for faixa in ["crianca", "adolescente", "adulto", "idoso"]:
    media = df[df["faixa_etaria"] == faixa]["imc"].mean()
    print(f"{faixa}: {round(media, 2)}")


# EXECUCAO DAS ANALISES PRINCIPAIS

analise_contagem_percentual(df)
analise_estatisticas(df)
analise_risco(df)

print("\nCodigo Encerrado e analise de IMC concluida!\n")
print("==================================================")

# REFERENCIAS UTILIZADAS

# ORGANIZACAO MUNDIAL DA SAUDE (OMS).
# A healthy lifestyle - WHO recommendations.
# Disponivel em: https://www.who.int/europe/news-room/fact-sheets/item/a-healthy-lifestyle---who-recommendations
# Acesso em: 20 abril. 2026.
#
# Os criterios de classificacao utilizados neste codigo foram baseados
# nas recomendacoes gerais da OMS para avaliacao de saude e estilo de vida.
