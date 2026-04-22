# Nome: Daniel Veiga Rodrigues de Faria
# Matrícula: 202603050
# E-mail Discente: daniel.veiga@discente.ufg.br
# Curso: Bacharelado em Inteligência Artificial
# Professor: Leonardo Antonio Alves

# GitHub: https://github.com/danivrf/Avaliacao_IP_BIA_2026_DanielVeiga/tree/main

## Resumo das Questões

### Questão 1
Nesta questão, utilizei a biblioteca **pandas** para a classificação de IMC. Empreguei `pd.to_datetime()` e o acessor `.dt` para calcular a idade a partir da data de nascimento. Usei o método `.describe()` para uma análise estatística inicial e `.apply()` com `axis=1` para aplicar funções personalizadas que classificam o IMC baseando-se em múltiplas colunas. Para consolidar os resultados, utilizei `groupby()` e `agg()` para calcular médias e medianas, além de `.value_counts()` e `.sort_values()` para organizar a distribuição das classificações. Também apliquei `pd.crosstab()` para gerar tabelas cruzadas e `isin()` para filtragem de grupos de risco, finalizando com um **loop** `for` para exibir os resultados por faixa etária.

### Questão 2
O foco desta questão foi a limpeza e análise epidemiológica com **pandas**. Utilizei métodos de string como `.str.strip()`, `.str.lower()` e `.str.title()` para padronização. A conversão de dados foi feita com `pd.to_numeric()` e `pd.to_datetime()`, usando `errors="coerce"` para identificar falhas. Tratei valores ausentes com `fillna()` (usando a mediana via `.median()`) e removi duplicatas com `.drop_duplicates()`. A lógica de alerta foi aplicada via `.apply()`, e a análise regional utilizou `groupby()`, `agg()` e `merge()` para unir tabelas de indicadores. Para as conclusões finais, empreguei `.idxmax()` para identificar extremos e `.sort_values()` para ordenar as taxas de incidência.

### Questão 3
Desenvolvi um sistema de gestão de estoque PEPS utilizando **dicionários** para armazenar os itens e **listas** para controlar os lotes de entrada. O código faz uso extensivo de **funções** e **loops** `while` para criar uma interface interativa com o usuário. Integrei a biblioteca **datetime** e **timedelta** para gerenciar cronogramas de reposição e prazos de compra. Para a parte estatística, utilizei **numpy** com funções como `np.sum()`, `np.mean()`, `np.argmax()` e `np.argmin()` para realizar cálculos rápidos sobre os saldos e giros de estoque. O relatório final é estruturado em um `pd.DataFrame()` do **pandas**, garantindo uma visualização organizada, e inclui rigorosas **validações** de entrada.

### Questão 4
Implementei o simulador "Primesweeper" focando em lógica algorítmica. Defini **funções** específicas para avaliar a primalidade dos números, utilizando um **loop** `for` com o operador `%` (resto da divisão) para identificar divisores. O programa conta com um modo interativo estruturado em um **loop** `while`, onde apliquei **validações** com `.isdigit()` para garantir que a entrada do usuário seja um número inteiro válido antes da conversão e processamento.

### Questão Extra
Nesta questão, como comentei dentro do próprio arquivo, foi baseada em um código que vi em um canal no YouTube, cujas devidas referências deixei no próprio programa. Criei uma versão interativa do jogo Sudoku. Utilizei a biblioteca **numpy** para gerenciar o tabuleiro como um **array**, facilitando a manipulação de matrizes e a verificação de regras em subgrades. A lógica central de validação foi estruturada em **funções** que percorrem linhas e colunas. Embora o código mencione o uso de **backtracking** como base conceitual para a resolução, a implementação foca na experiência do usuário através de um **loop** interativo, processamento de strings com `.split()` e diversas **validações** para garantir a integridade das jogadas realizadas no terminal.