"""
Solução do Projeto do Módulo 13 - Fundamentos da Descoberta de Dados
Análise de dados de produtos de um supermercado.
"""

import pandas as pd
import plotly.express as px

# --- Leitura e Preparação dos Dados ---

# O arquivo CSV deve estar no mesmo diretório que este script,
# ou o caminho completo para o arquivo deve ser fornecido.
try:
    df = pd.read_csv("C:/Users/pimen/Downloads/MODULO7_PROJETOFINAL_BASE_SUPERMERCADO - MODULO7_PROJETOFINAL_BASE_SUPERMERCADO (1).csv.csv", delimiter=',')
except FileNotFoundError:
    print("Erro: O arquivo CSV não foi encontrado.")
    print("Por favor, verifique se o nome e o caminho do arquivo estão corretos.")
    exit()

print("Visualização inicial dos dados:")
print(df.head())
print("\n" + "="*50 + "\n")

# Para análises estatísticas de preço, é importante remover produtos com Preco_Normal = 0,
# pois eles podem representar dados ausentes ou itens promocionais sem preço de referência,
# o que distorceria cálculos como média e desvio padrão.
df_precos_validos = df[df['Preco_Normal'] > 0].copy()


# --- # 1 - Média e Mediana dos Preços por Categoria ---

print("# 1 - Média e Mediana dos Preços por Categoria\n")

# Agrupando por categoria e calculando a média e a mediana
preco_stats = df_precos_validos.groupby('Categoria')['Preco_Normal'].agg(['mean', 'median'])

# Formatando para melhor visualização
preco_stats['mean'] = preco_stats['mean'].round(2)
preco_stats['median'] = preco_stats['median'].round(2)

print("Média e Mediana do Preço Normal por Categoria:")
print(preco_stats)
print("\n")

print("Análise (Média vs. Mediana):")
print("""
- **Categorias com Média Acima da Mediana:** 'belleza-y-cuidado-personal', 'lacteos', 'congelados', 'comidas-preparadas'.
  Isso indica uma distribuição assimétrica à direita, onde alguns produtos com preços muito altos elevam a média em relação à mediana.

- **Categorias com Média Próxima da Mediana:** 'frutas', 'verduras', 'instantaneos-y-sopas'.
  Nestas categorias, os preços são distribuídos de forma mais simétrica.
""")
print("\n" + "="*50 + "\n")


# --- # 2 - Desvio Padrão por Categoria ---

print("# 2 - Desvio Padrão por Categoria\n")

# Calculando o desvio padrão do Preco_Normal
desvio_padrao = df_precos_validos.groupby('Categoria')['Preco_Normal'].std().round(2).sort_values(ascending=False)

print("Desvio Padrão do Preço Normal por Categoria:")
print(desvio_padrao)
print("\n")

print("Análise (Comportamento nas Categorias com Maior Desvio):")
print("""
A categoria com o maior desvio padrão é 'belleza-y-cuidado-personal' (2884.22), seguida por 'lacteos' (2848.51).
Um desvio padrão alto significa que os preços dos produtos dentro dessa categoria variam muito.

Como observado na Questão 1, nessas duas categorias a média é significativamente maior que a mediana.
Isso confirma que a grande variação de preços (alto desvio padrão) é provavelmente causada por alguns itens de valor muito elevado, que "puxam" a média para cima.
""")
print("\n" + "="*50 + "\n")


# --- # 3 - Boxplot da Categoria com Maior Desvio Padrão ---

print("# 3 - Boxplot da Categoria com Maior Desvio Padrão\n")

# Identificando a categoria com maior desvio padrão
categoria_maior_desvio = desvio_padrao.idxmax()
print(f"A categoria com maior desvio padrão é: '{categoria_maior_desvio}'\n")

# Filtrando o DataFrame para essa categoria
df_categoria_maior_desvio = df_precos_validos[df_precos_validos['Categoria'] == categoria_maior_desvio]

# Criando o boxplot com Plotly Express
fig_boxplot = px.box(
    df_categoria_maior_desvio,
    y='Preco_Normal',
    title=f'Distribuição de Preços para a Categoria: {categoria_maior_desvio}',
    points="all"  # Mostra todos os pontos de dados
)

print("Gerando o gráfico de Boxplot... (uma janela do navegador pode ser aberta)")
fig_boxplot.show()

print("\nAnálise do Boxplot:")
print("""
O boxplot da categoria 'belleza-y-cuidado-personal' mostra:
- **Concentração de Dados:** A maioria dos produtos tem preços concentrados na parte inferior do gráfico (a "caixa" é relativamente pequena e baixa).
- **Assimetria à Direita:** A linha da mediana está na parte inferior da caixa, e a "cauda" superior é muito longa, confirmando a assimetria.
- **Muitos Outliers:** Há uma grande quantidade de pontos (outliers) acima do limite superior do boxplot. Isso representa produtos com preços muito mais altos que a maioria, como pacotes de fraldas e kits de shampoo, que elevam a média e o desvio padrão.
""")
print("\n" + "="*50 + "\n")


# --- # 4 - Gráfico de Barras com a Média de Descontos por Categoria ---

print("# 4 - Gráfico de Barras com a Média de Descontos por Categoria\n")

# Agrupando e calculando a média de descontos
media_descontos = df.groupby('Categoria')['Desconto'].mean().round(2).sort_values(ascending=False)

print("Média de Descontos por Categoria:")
print(media_descontos)

# Criando o gráfico de barras
fig_barras = px.bar(
    media_descontos,
    x=media_descontos.index,
    y=media_descontos.values,
    title='Média de Descontos por Categoria',
    labels={'x': 'Categoria', 'y': 'Média de Desconto (em $)'},
    text=media_descontos.values
)

print("\nGerando o gráfico de Barras... (uma janela do navegador pode ser aberta)")
fig_barras.show()
print("\n" + "="*50 + "\n")


# --- # 5 - Gráfico de Treemap Interativo (Média de Desconto por Categoria e Marca) ---

print("# 5 - Gráfico de Treemap Interativo\n")

# Para evitar problemas com a agregação, vamos garantir que temos apenas valores positivos de desconto.
df_descontos = df[df['Desconto'] > 0]

# Agregando os dados para o treemap. Usaremos a média de desconto.
# Como pode haver muitas marcas, o treemap pode ficar bem denso.
# O reset_index() transforma o resultado agrupado de volta em um DataFrame.
treemap_data = df_descontos.groupby(['Categoria', 'Marca'])['Desconto'].mean().reset_index()

# Criando o treemap interativo
fig_treemap = px.treemap(
    treemap_data,
    path=[px.Constant("Todas as Categorias"), 'Categoria', 'Marca'],
    values='Desconto',
    color='Desconto',
    hover_data={'Desconto': ':.2f'},
    color_continuous_scale='YlGnBu',
    title='Média de Desconto por Categoria e Marca'
)

fig_treemap.update_layout(margin = dict(t=50, l=25, r=25, b=25))

print("Gerando o gráfico de Treemap... (uma janela do navegador pode ser aberta)")
fig_treemap.show()
print("\n" + "="*50 + "\n")