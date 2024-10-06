"""
IMPORTANTE: PARA MELHOR VIZUALICAÇÃO E ENTENDIMENTO DO CÓDIGO, RECOMENDO ANÁLISE VIA O ARQUIVO .IPYNB
"""

import pandas as pd
import matplotlib.pyplot as plt

# Carregando o dataset
df = pd.read_csv('netflix_titles.csv')
print(df.head())


# Quais colunas estão presentes no dataset?
print(f"O dataset possui {len(df.columns)} colunas")

# Quantos filmes estão disponíveis na Netflix?
print(df['type'].unique())

df_movies = df[df['type'] == 'Movie']
filmes_unicos = df_movies['title'].unique()

print(f"\nA netflix possui {len(filmes_unicos)} filmes disponíveis")

# Quem são os 5 diretores com mais filmes e séries na plataforma?
df_directos_movie = df['director'].value_counts().head(5)

print("Os 5 diretores com mais obras são:")

for key, value in df_directos_movie.items():
    print(f"{key} - {value} obras")

# Quais diretores também atuaram como atores em suas próprias produções?

# Conversão da coluna cast para o formato de lista
df['cast'] = df['cast'].apply(lambda x: x.split(", ") if pd.notnull(x) else [])

#Criação de um dataset em que somente há diretores que tambem atuam
list_directors_actors = df[df.apply(lambda row: row['director'] in row['cast'], axis=1)]

# Agrupa os diretores e as os titulos de suas obras
directors_titles = list_directors_actors.groupby('director')['title'].apply(list)

# cria uma contagem de diretores e a quantidade de obras em que também atuaram
directors_counts = directors_titles.apply(len)
top_directors = directors_counts.sort_values(ascending=False)

print(top_directors.head(5))

# Print a quantiadade de diretores que dirigiram suas obras, bem como seus nomes e obras trabalhadas
print(f"Temos um total de {len(top_directors)} diretores que também trabalham como atores\n")
for director in top_directors.index:
    print(f"{director} ({top_directors[director]} obras):")
    for title in directors_titles[director]:
        print(f" - {title}")

    print(" ")

# Análise Rating das obras
adults = ['TV-MA', 'R', 'NC-17']
childs = ['PG-13', 'PG', 'TV-14', 'TV-PG', 'TV-Y', 'TV-Y7', 'TV-G', 'G', 'TV-Y7-FV']

adults_count = df[df['rating'].isin(adults)].shape[0]
childs_count = df[df['rating'].isin(childs)].shape[0]

print(f"Quantidade de filmes para maiores de 17 (Com alguma restrição): {adults_count}")
print(f"Quantidade de filmes para crianças ou todos os públicos: {childs_count}")

# Plot do gráfico de pizza
plt.figure(figsize=(7, 7))
plt.pie([adults_count, childs_count], labels=['Adults', 'Childs'], autopct='%1.1f%%')
plt.title('Distribuição de filmes/programas de TV para adultos e crianças')
plt.show()

# Análise tipos de conteúdo

# Converte para o formato de lista a string de gêneros
df['listed_in'] = df['listed_in'].apply(lambda x: x.split(", ") if pd.notnull(x) else [])

all_categories = df['listed_in'].explode()

category_counts = all_categories.value_counts()
category_counts = category_counts[~category_counts.index.isin(['International Movies', 'International TV Shows', 'Movies', ''])]

# Plot em barras do gênero
plt.figure(figsize=(10, 6))
category_counts.plot(kind='bar', color='#66b3ff')
plt.title('Quantidade de obras por Categoria')
plt.xlabel('Categorias')
plt.ylabel('Quantidade')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Crescimento dos filmes LGBTQ ao longo dos anos

lgbt_movies = df[df.apply(lambda row: 'LGBTQ Movies' in row['listed_in'], axis=1)]
movies_per_year = lgbt_movies['release_year'].value_counts().sort_index()

# Plot gráfico de barras para a quantidade de filmes por ano
plt.figure(figsize=(10, 6))
ax = movies_per_year.plot(kind='bar', color='#66b3ff')
plt.title('Quantidade de Filmes por Ano')
plt.xlabel('Ano de Lançamento')
plt.ylabel('Quantidade de Filmes')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()


