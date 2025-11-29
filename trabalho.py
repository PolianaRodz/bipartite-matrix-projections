# Imports para manipulação de dados (Pandas), álgebra linear (NumPy) e análise visual de grafos (NetworkX/Matplotlib).
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os 

# funçao para criar a pasta que salvará as imagens dos grafos, para manter o projeto organizado.
pasta_saida = "resultados"
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)
    print(f"Pasta '{pasta_saida}' verificada.")


# CARREGAMENTO E TRATAMENTO DE DADOS


arquivo = 'dataset_tecnologias.csv'

try:
    # Tenta ler o arquivo com vírgula (padrão internacional)
    df_raw = pd.read_csv(arquivo, sep=',')
    
    # Se detectar poucas colunas, tenta ler com ponto e vírgula 
    if df_raw.shape[1] < 3:
        df_raw = pd.read_csv(arquivo, sep=';')
    
    # Padroniza os nomes das colunas para evitar erros de digitação no CSV
    # Coluna 0: Aluno (Source), Coluna 1: Tecnologia (Target), Coluna 2: Peso
    df_raw.columns = ['from', 'to', 'weight']
    
    # Validação simples dos requisitos (10 alunos, 4 tecnologias)
    if df_raw['from'].nunique() < 10 or df_raw['to'].nunique() < 4:
        print("⚠️ AVISO: O dataset parece menor que o exigido (Min: 10 alunos, 4 techs).")

    # Transforma a lista de dados em uma Matriz de Incidência (Pivot Table)
    # Linhas = Alunos, Colunas = Tecnologias, Valores = Peso (1 ou 0)
    df = df_raw.pivot_table(index='from', columns='to', values='weight', fill_value=0)
    print(f"Dataset carregado com sucesso: {df.shape[0]} Alunos x {df.shape[1]} Tecnologias")

except Exception as e:
    print(f" Erro  ao ler o arquivo: {e}")
    exit()


# GERAÇÃO DAS MATRIZES 

print("Calculando matrizes...")

# A - Matriz de Incidência (Alunos x Tecnologias)
# Representa a relação direta de quem escolheu o quê.
matriz_incidencia = df

# B - Matriz de Similaridade (Alunos x Alunos)
# Multiplicação da matriz pela sua transposta (A * A^T).
# O resultado mostra quantos itens em comum dois alunos têm.
matriz_similaridade = df.dot(df.T)
np.fill_diagonal(matriz_similaridade.values, 0) # Remove a relação do aluno com ele mesmo

# C - Matriz de Coocorrência (Tecnologias x Tecnologias)
# Multiplicação da transposta pela matriz original (A^T * A).
# O resultado mostra quantas vezes duas tecnologias foram escolhidas juntas.
matriz_coocorrencia = df.T.dot(df)
np.fill_diagonal(matriz_coocorrencia.values, 0) # Remove a relação da tech com ela mesma


# FUNÇÃO DE PLOTAGEM E ANÁLISE.

def analisar_grafo(grafo, titulo, nome_arquivo, bipartido=False):
    plt.figure(figsize=(10, 8))
    
    # Definição do Layout (Organização visual dos nós)
    if bipartido:
        # Separa os nós em dois grupos (Alunos de um lado, Techs do outro)
        top = nx.bipartite.sets(grafo)[0]
        pos = nx.bipartite_layout(grafo, top)
        cor = 'lightblue' # Cor para incidência
    else:
        # Layout de força (nós conectados ficam perto)
        pos = nx.spring_layout(grafo, seed=42)
        cor = 'lightgreen' # Cor para similaridade/coocorrência

    # Desenha o grafo
    weights = [grafo[u][v].get('weight', 1) for u,v in grafo.edges()]
    nx.draw(grafo, pos, with_labels=True, node_color=cor, node_size=2000, 
            font_weight='bold', width=[w*0.5 for w in weights], edge_color='gray')
    
    # Salva o arquivo
    caminho_final = os.path.join(pasta_saida, nome_arquivo)
    plt.title(titulo)
    plt.savefig(caminho_final) 
    print(f"> Grafo salvo: {caminho_final}")

    # Cálculo de Métrica: Centralidade de Grau (Popularidade)
    # Identifica o nó com maior número de conexões diretas
    try:
        cent = nx.degree_centrality(grafo)
        top_no = max(cent, key=cent.get)
        print(f"  • Nó Central (Mais conectado): {top_no} ({cent[top_no]:.2f})")
    except:
        pass
    
    plt.close()
    print("-" * 30)


# EXECUÇÃO E GERAÇÃO DOS RESULTADOS.

print("\n--- Iniciando Geração dos Grafos ---")

# Grafo de Incidência (Bipartido)
G_inc = nx.Graph()
G_inc.add_nodes_from(df.index, bipartite=0)
G_inc.add_nodes_from(df.columns, bipartite=1)
# Adiciona arestas onde o valor na matriz é >= 1
rows, cols = np.where(df >= 1)
G_inc.add_edges_from(zip(df.index[rows], df.columns[cols]))
analisar_grafo(G_inc, "Grafo de Incidência", "grafo_incidencia.png", bipartido=True)

# Grafo de Similaridade (Rede de Alunos)
G_sim = nx.from_pandas_adjacency(matriz_similaridade)
analisar_grafo(G_sim, "Grafo de Similaridade (Entre Alunos)", "grafo_similaridade.png")

# Grafo de Coocorrência (Rede de Tecnologias)
G_cooc = nx.from_pandas_adjacency(matriz_coocorrencia)
analisar_grafo(G_cooc, "Grafo de Coocorrência (Entre Tecnologias)", "grafo_coocorrencia.png")

print("Processo concluído com sucesso!")