'''
Esse código diferente do código "christofies_simplificado" foca na robustez da implementação, no código anterior foram usados 
dicionários de listas de tuplas para facilitar o entendimento, as chaves eram os vértices e a lista de valores eram as arestas, com destino e peso,
neste código, o grafo de entrada, completo e não direcionado será representado como uma matriz de adjacências usando matriz normal, e não como
uma lista de adjacências, essa é a representação ideal para grafos densos (mais robusto). Nas estruturas seguintes do algoritmo, como a árvore geradora mínima
e em certas partes de funções para acessar o grafo original que agora é uma matriz, serão ligeiramente diferentes. A árvore será representada agora
como um dicionário de dicionário de inteiros, a chave do primeiro dicionario representam os vértices, os sub-dicionários as arestas (mais especificamente o destino),
e os valores inteiros os pesos, a lógica das funções e o fluxo do programa continua o mesmo, prim, hierholzer, emparelhamento etc...
'''
import networkx as nx
import heapq

def leitura_arquivo(caminho: str):
    with open(caminho, 'r') as f:
        linhas = f.read().splitlines()

    n = int(linhas[0])
    matriz = []

    for i in range(n):
        linha = list(map(int, linhas[i + 1].split()))
        matriz.append(linha)

    return matriz # retorna direto a matriz como matriz de adjacencias

def prim(grafo):
    vertices = len(grafo)
    visitados = set() 
    mst = {v: {} for v in range(vertices)}

    start = 0
    visitados.add(start)

    heap = [] 
    for j in range(vertices):
         heapq.heappush(heap, (grafo[start][j], start, j)) # peso, origem, destino

    while heap:
        peso, origem, destino = heapq.heappop(heap)
        if destino not in visitados:
            visitados.add(destino)
            mst[origem][destino] = peso
            mst[destino][origem] = peso
            for aresta in range(vertices):
                if aresta not in visitados:
                    if aresta != destino:
                     heapq.heappush(heap, (grafo[destino][aresta], destino, aresta)) # peso, origem, destino
                    
    return mst

def vertices_impares(arvore_geradora):
    return [v for v, adj in arvore_geradora.items() if len(adj) % 2 != 0]

def grafo_auxiliar(grafo, vertices):
    G = nx.Graph()
    for u in vertices:
        for v in vertices:
            if u != v:
                peso = grafo[u][v]
                G.add_edge(u, v, weight=peso)
    return G

def ciclo_euleriano(grafo):
    circuito = []
    start = next(iter(grafo))
    
    stack = [start]
    while stack:
        atual = stack[-1]
        if grafo[atual]:
            proxima = next(iter(grafo[atual]))
            del grafo[atual][proxima]
            del grafo[proxima][atual]
            
            stack.append(proxima)
        else:
            circuito.append(stack.pop())
    return circuito

def ciclo_hamiltoniano(circuito):
    visitados = set()
    caminho = []
    for v in circuito:
        if v not in visitados:
            visitados.add(v)
            caminho.append(v)
    caminho.append(caminho[0])
    return caminho

def custo_total(grafo, ciclo):
    total = 0
    for i in range(len(ciclo) - 1):
        origem = ciclo[i]
        destino = ciclo[i + 1]
        peso = grafo[origem][destino]
        total += peso
    return total

def christofides():
    grafo = leitura_arquivo("grafo.txt")
    mst = prim(grafo)
    impares = vertices_impares(mst)
    aux = grafo_auxiliar(grafo, impares)
    emparelhamento = nx.algorithms.matching.min_weight_matching(aux)

    for u, v in emparelhamento:
        mst[u][v] = grafo[u][v]
        mst[v][u] = grafo[u][v]

    circuito = ciclo_euleriano(mst)
    ciclo_final = ciclo_hamiltoniano(circuito)
    custo = custo_total(grafo, ciclo_final)

    print(" -> ".join(map(str, ciclo_final)))
    print(f"Peso total do ciclo hamiltoniano: {custo}")

if __name__ == "__main__":
    christofides()