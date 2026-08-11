#%%
import pandas as pd

df_orders = pd.read_csv('orders.csv')
df_order_details = pd.read_csv('order_details.csv')
df_pizzas = pd.read_csv('pizzas.csv')
df_pizza_types = pd.read_csv('pizza_types.csv', encoding='latin1')

# %%
# --- TRATAMENTO E NORMALIZAÇÃO ---

# 2. Criar a Tabela 'categories'
categories_list = df_pizza_types['category'].unique()
df_categories = pd.DataFrame({'category_name': categories_list})
# Criando um ID sequencial para as categorias
df_categories['category_id'] = range(1, len(df_categories) + 1) 
df_categories = df_categories[['category_id', 'category_name']] # Reorganizando as colunas

# %%
# 3. Atualizar a Tabela 'pizza_types' (Substituindo texto por category_id)
df_pizza_types = df_pizza_types.merge(df_categories, left_on='category', right_on='category_name')
# Selecionar apenas as colunas que importam para a nova tabela
df_pizza_types_clean = df_pizza_types[['pizza_type_id', 'name', 'category_id']]
# %%
# 4. Criar a Tabela 'ingredients' e a Associativa 'pizza_type_ingredients'
# Primeiro, pegamos a coluna de ingredientes e quebramos a string pelas vírgulas
df_ingredients_temp = df_pizza_types[['pizza_type_id', 'ingredients']].copy()
df_ingredients_temp['ingredients'] = df_ingredients_temp['ingredients'].str.split(',')
# %%
# 'explode' transforma a lista de ingredientes em várias linhas, repetindo o pizza_type_id
df_exploded = df_ingredients_temp.explode('ingredients')
# Remover espaços em branco que ficam no início/fim das palavras após separar por vírgula
df_exploded['ingredients'] = df_exploded['ingredients'].str.strip()
# Padronização:*
df_exploded['ingredients'] = df_exploded['ingredients'].replace('Artichoke', 'Artichokes')
# %%# --- APLICAÇÃO DAS REGRAS DE NEGÓCIO ---
# 4.1. Adicionar Mozzarella Cheese em todas as pizzas que ainda não possuem
mozzarella_pizzas = pd.DataFrame({
    'pizza_type_id': df_pizza_types['pizza_type_id'],
    'ingredients': 'Mozzarella Cheese'})

# 4.2. Adicionar Tomato Sauce apenas onde não há outro molho ("Sauce") especificado
# Filtragem das pizzas que NÃO contém a palavra 'Sauce' nos ingredientes originais
pizzas_sem_molho = df_pizza_types[~df_pizza_types['ingredients'].str.contains('Sauce', case=False)]
tomato_pizzas = pd.DataFrame({
    'pizza_type_id': pizzas_sem_molho['pizza_type_id'],
    'ingredients': 'Tomato Sauce'})

# Unir os ingredientes originais com as novas regras e remover duplicatas (caso já houvesse queijo na lista)
df_exploded = pd.concat([df_exploded, mozzarella_pizzas, tomato_pizzas]).drop_duplicates()



#%%
# Extração dos ingredientes únicos para a tabela definitiva de Ingredientes
unique_ingredients = df_exploded['ingredients'].unique()
df_ingredients = pd.DataFrame({'ingredient_name': unique_ingredients})
df_ingredients['ingredient_id'] = range(1, len(df_ingredients) + 1)
df_ingredients = df_ingredients[['ingredient_id', 'ingredient_name']]
# %%
# Criar a tabela associativa cruzando os dados explodidos com os IDs gerados
df_pizza_type_ingredients = df_exploded.merge(df_ingredients, left_on='ingredients', right_on='ingredient_name')
df_pizza_type_ingredients = df_pizza_type_ingredients[['pizza_type_id', 'ingredient_id']]
# %%


#%%
print("--- INICIANDO AUDITORIA DE DADOS ---")

# 1. Validação: orders
print("\n[1] Verificando df_orders...")
# NOT NULL e UNIQUE para order_id
print(f" - order_id Nulos: {df_orders['order_id'].isnull().sum()}")
print(f" - order_id Duplicados: {df_orders['order_id'].duplicated().sum()}")
print(f" - date Nulos: {df_orders['date'].isnull().sum()}")
print(f" - time Nulos: {df_orders['time'].isnull().sum()}")
#%%
# CHECK (date >= '2015-01-01' AND date <= '2015-12-31')
# Convertendo para datetime temporariamente para garantir a checagem
datas_invalidas = pd.to_datetime(df_orders['date']).loc[
    ~pd.to_datetime(df_orders['date']).between('2015-01-01', '2015-12-31')
]
print(f" - Datas fora do intervalo (2015): {len(datas_invalidas)}")

#%%
# 2. Validação: order_details
print("\n[2] Verificando df_order_details...")
print(f" - order_details_id Nulos: {df_order_details['order_details_id'].isnull().sum()}")
print(f" - order_details_id Duplicados: {df_order_details['order_details_id'].duplicated().sum()}")
print(f" - order_id Nulos: {df_order_details['order_id'].isnull().sum()}")
print(f" - pizza_id Nulos: {df_order_details['pizza_id'].isnull().sum()}")
print(f" - quantity Nulos: {df_order_details['quantity'].isnull().sum()}")

# CHECK (quantity > 0)
qtd_invalida = df_order_details[df_order_details['quantity'] <= 0]
print(f" - Quantidades <= 0: {len(qtd_invalida)}")

#%%
# 3. Validação: pizzas
print("\n[3] Verificando df_pizzas...")
print(f" - pizza_id Nulos: {df_pizzas['pizza_id'].isnull().sum()}")
print(f" - pizza_id Duplicados: {df_pizzas['pizza_id'].duplicated().sum()}")
print(f" - pizza_type_id Nulos: {df_pizzas['pizza_type_id'].isnull().sum()}")
print(f" - size Nulos: {df_pizzas['size'].isnull().sum()}")
print(f" - price Nulos: {df_pizzas['price'].isnull().sum()}")

# CHECK (size IN ('S', 'M', 'L', 'XL', 'XXL'))
tamanhos_validos = ['S', 'M', 'L', 'XL', 'XXL']
tamanho_invalido = df_pizzas[~df_pizzas['size'].isin(tamanhos_validos)]
print(f" - Tamanhos fora do padrão: {len(tamanho_invalido)}")

# CHECK (price > 0)
preco_invalido = df_pizzas[df_pizzas['price'] <= 0]
print(f" - Preços <= 0: {len(preco_invalido)}")

#%%
# 4. Validação: pizza_types (usando df limpo)
print("\n[4] Verificando df_pizza_types_clean...")
print(f" - pizza_type_id Nulos: {df_pizza_types_clean['pizza_type_id'].isnull().sum()}")
print(f" - pizza_type_id Duplicados: {df_pizza_types_clean['pizza_type_id'].duplicated().sum()}")
print(f" - name Nulos: {df_pizza_types_clean['name'].isnull().sum()}")
print(f" - name Duplicados: {df_pizza_types_clean['name'].duplicated().sum()}")
print(f" - category_id Nulos: {df_pizza_types_clean['category_id'].isnull().sum()}")

#%%
# 5. Validação: categories
print("\n[5] Verificando df_categories...")
print(f" - category_id Nulos: {df_categories['category_id'].isnull().sum()}")
print(f" - category_id Duplicados: {df_categories['category_id'].duplicated().sum()}")
print(f" - category_name Nulos: {df_categories['category_name'].isnull().sum()}")
print(f" - category_name Duplicados: {df_categories['category_name'].duplicated().sum()}")

#%%
# 6. Validação: ingredients
print("\n[6] Verificando df_ingredients...")
print(f" - ingredient_id Nulos: {df_ingredients['ingredient_id'].isnull().sum()}")
# Se a tabela de ingredientes original foi montada pelo 'unique()', já não tem duplicados, mas validamos:
print(f" - ingredient_id Duplicados: {df_ingredients['ingredient_id'].duplicated().sum()}")
print(f" - ingredient_name Nulos: {df_ingredients['ingredient_name'].isnull().sum()}")

#%%
# 7. Validação: pizza_type_ingredients (Tabela Associativa)
print("\n[7] Verificando df_pizza_type_ingredients...")
print(f" - pizza_type_id Nulos: {df_pizza_type_ingredients['pizza_type_id'].isnull().sum()}")
print(f" - ingredient_id Nulos: {df_pizza_type_ingredients['ingredient_id'].isnull().sum()}")

# UNIQUE composto: Verifica se existe a mesma combinação de pizza e ingrediente mais de uma vez
duplicatas_compostas = df_pizza_type_ingredients.duplicated(subset=['pizza_type_id', 'ingredient_id']).sum()
print(f" - Combinações Pizza+Ingrediente duplicadas: {duplicatas_compostas}")
#%%
print("\n--- FIM ---")
# %%
#%% --- INGESTÃO NO SQL SERVER (DOCKER) ---
from sqlalchemy import create_engine
import urllib

# Garante que caracteres especiais na senha não quebrem a conexão
password_encoded = urllib.parse.quote_plus("SenhaForte@2026!")

# String de Conexão
connection_string = (
    f"mssql+pyodbc://sa:{password_encoded}@127.0.0.1:1433/PizzaSales"
    "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

engine = create_engine(connection_string)

# Dicionário mapeando as tabelas do banco -> DataFrames
# A ORDEM É OBRIGATÓRIA para respeitar as FK
dataframes_to_load = {
    'categories': df_categories,            # 1º (Base)
    'pizza_types': df_pizza_types_clean,    # 2º (Depende de Categories)
    'ingredients': df_ingredients,          # 3º (Base)
    'pizza_type_ingredients': df_pizza_type_ingredients, # 4º (Depende de PizzaTypes e Ingredients)
    'pizzas': df_pizzas,                    # 5º (Depende de PizzaTypes)
    'orders': df_orders,                    # 6º (Independente)
    'order_details': df_order_details       # 7º (Depende de Orders e Pizzas)
}

print("--- INICIANDO CARGA NO SQL SERVER ---")

for table_name, df in dataframes_to_load.items():
    try:
        print(f"Enviando {table_name} ({len(df)} registros)...")
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"[OK] {table_name} carregado com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar {table_name}: {e}")

print("\n[OK] Carga finalizada com sucesso! Os dados agora residem no SQL Server.")