'''
Esse código diferente do código "christofies_simplificado" foca na robustez da implementação, no código anterior foram usados 
dicionários de listas de tuplas para facilitar o entendimento, as chaves eram os vértices e a lista de valores eram as arestas, com destino e peso,
neste código, o grafo de entrada, completo e não direcionado será representado como uma matriz de adjacências usando matriz normal, e não como
uma lista de adjacências, essa é a representação ideal para grafos densos (mais robusto). A lógica das funções e o fluxo do programa continua o mesmo, prim, hierholzer,
emparelhamento etc...
'''
import networkx as nx
import heapq
import matplotlib.pyplot as plt
import math

def leitura_arquivo(caminho: str):
    with open(caminho, 'r') as f:
        linhas = f.read().splitlines()

    n = int(linhas[0])
    matriz = []

    for i in range(n):
        linha = list(map(float, linhas[i + 1].split()))
        matriz.append(linha)

    return matriz

def prim(grafo):
    vertices = list(range(len(grafo)))
    visitados = set()
    mst = {v: [] for v in vertices}

    inicio = vertices[0]
    visitados.add(inicio)

    heap = []
    for destino in vertices:
        if destino not in visitados:
            heapq.heappush(heap, (grafo[inicio][destino], inicio, destino))  # (peso, origem, destino)

    while heap:
        peso, origem, destino = heapq.heappop(heap)
        if destino not in visitados:
            visitados.add(destino)
            mst[origem].append((destino, peso))
            mst[destino].append((origem, peso))
            for aresta in vertices:
                    if aresta not in visitados:
                        heapq.heappush(heap, (grafo[destino][aresta], destino, aresta))  # (peso, origem, destino)

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
    stack = [0]

    while stack:
        atual = stack[-1]
        if grafo[atual]:
            proxima = grafo[atual].pop(0)
            grafo[proxima[0]].remove((atual, proxima[1]))
            stack.append(proxima[0])
        else:
            circuito.append(stack.pop())
    return circuito

def ciclo_hamiltoniano(circuito):
    ciclo = []
    for v in circuito:
        if v not in ciclo:
            ciclo.append(v)
    ciclo.append(ciclo[0])
    return ciclo

def custo_total(G, grafo, ciclo):
    total = 0.0
    for i in range(len(ciclo) - 1):
        origem = ciclo[i]
        destino = ciclo[i + 1]
        peso = grafo[origem][destino]
        total += peso
        G.add_edge(origem, destino, weight=peso)

    return total, G

def christofides():
    grafo = leitura_arquivo("grafo2.txt")
    mst = prim(grafo)

    print("Arvore geradora minima: \n")
    print(mst)
    peso_mst = 0.0
    for v in mst.values():
        for (_, p) in v:
            peso_mst += p

    print(f"\nPeso total da Arvore geradora Minima: {peso_mst / 2}\n")

    impares = vertices_impares(mst)
    aux = grafo_auxiliar(grafo, impares)
    emparelhamento = nx.algorithms.matching.min_weight_matching(aux)

    for u, v in emparelhamento:
        peso = grafo[u][v]
        mst[u].append((v, peso))
        mst[v].append((u, peso))

    circuito = ciclo_euleriano(mst)
    ciclo_final = ciclo_hamiltoniano(circuito)
    G = nx.Graph()
    custo, G = custo_total(G, grafo, ciclo_final)

    print("Solucao aproximada encontrada por Christofides: ")
    print(" -> ".join(map(str, ciclo_final)))
    print(f"\nPeso total da solucao: {custo}\n")

    raiz = 10 / math.sqrt(len(grafo))
    pos = nx.spring_layout(G, seed=81, k=raiz, scale=10)
    edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in G.edges(data=True)}

    plt.figure(figsize=(12, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='blue', node_size=500, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    christofides()