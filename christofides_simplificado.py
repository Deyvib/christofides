import networkx as nx
import heapq

def leitura_arquivo(caminho: str): # simplesmente lê o arquivo txt, passa para matriz para facilitar o acesso, e joga para um dicionario que será nossa lista de adjacências
    with open(caminho, 'r') as f:
        linhas = f.read().splitlines()

    n = int(linhas[0]) # pega o número de vértices, padrão como a primeira linha do arquivo.txt conforme descrito no trabalho
    matriz = []
    grafo = {v + 1: [] for v in range(n)} # inicializa o dicionário com uma compressão de dicionários

    for i in range(n):
        linha = list(map(int, linhas[i + 1].split()))
        matriz.append(linha)

    for i in range(n):
        for j in range(n):
            if i != j:
                grafo[i + 1].append((j + 1, matriz[i][j])) # preenche o dicionário

    return grafo

def prim(grafo): # algoritmo de prim para pegar a árvore geradora mínima do grafo completo
    vertices = list(grafo.keys()) # pega a lista de vértices que é a mesma coisa que as chaves do dicionário
    visitados = set() # uma estrutura de dados hashset para apenas verificar os vértices já visitados no prim, útil para a verificação de se um ciclo será formado
    mst = {v: [] for v in vertices} # inicializa um dicionario com compressão, mst representará nossa árvore geradora mínima

    start = vertices[0] # escolhe um vértice qualquer, nesse caso o primeiro
    visitados.add(start) # e o adiciona na lista de já visitados

    heap = []
    for aresta in grafo[start]: # preenche o heap mínimo com as arestas que saem do vértice inicial
        heapq.heappush(heap, (aresta[1], start, aresta[0]))  # (peso, origem, destino)

    while heap: # implementação do algoritmo de prim
        peso, origem, destino = heapq.heappop(heap)
        if destino not in visitados:
            visitados.add(destino)
            mst[origem].append((destino, peso)) # preenche a árvore geradora com o novo vertice bidirecionalmente
            mst[destino].append((origem, peso))
            for aresta in grafo[destino]:
                if aresta[0] not in visitados:
                    heapq.heappush(heap, (aresta[1], destino, aresta[0]))  # (peso, origem, destino)

    return mst

def vertices_impares(arvore_geradora):
    return [v for v, adj in arvore_geradora.items() if len(adj) % 2 != 0] # usa compressão de listas para retornar uma lista com os vertices com graus impares
# perceba que um dicionario é uma tupla (key, value) o valor é uma lista de tuplas nesse código, representando as arestas, tamanho da lista (quantidade de aresta) é impar? então o vértice tem grau impar

def grafo_auxiliar(grafo, vertices): # para usar a função de emparelhamento da biblioteca, precisa-se criar um grafo do tipo nx.Graph especificando o peso, só serve para retornar... ->
    G = nx.Graph() # uma estrutura válida que a função aceite como parâmetro para retornar o emparelhamento válido
    for u in vertices:
        for v in vertices:
            if u != v:
                peso = next(p for d, p in grafo[u] if d == v) # encontra o primeiro elemento p, do conjunto de chaves e valores do dicionario onde a chave seja igual a v, ou seja, o peso da aresta u, v
                G.add_edge(u, v, weight=peso) # é obrigatorio especificar o atributo "weight" só assim a função de emparelhamento vai saber o valor do peso para usar
    return G

def ciclo_euleriano(grafo): # algoritmo para achar o ciclo euleriano na arvore geradora + o emparelhamento (não é do hierholzer, mas uma variação simples dele)
    circuito = []
    stack = [next(iter(grafo))]

    while stack: # simplesmente vai seguindo as arestas até ficar sem saída, colocando numa pilha, se não tem pra onde ir, adiciona o vertice atual no circuito
        atual = stack[-1]
        if grafo[atual]:
            proxima = grafo[atual].pop(0)
            grafo[proxima[0]].remove((atual, proxima[1]))
            stack.append(proxima[0])
        else:
            circuito.append(stack.pop())
    return circuito # essa função constroi o ciclo de trás pra frente, como você garantiu os vertices terem grau par anteriormente, é garantido retornar um ciclo euleriano

def ciclo_hamiltoniano(circuito): # essa é uma das funções mais simples junto com a de pegar os vertices impares, basicamente vai iterar sobre o circuito euleriano (lista de vertices)
    visitados = set()
    caminho = []
    for v in circuito:
        if v not in visitados:
            visitados.add(v)
            caminho.append(v)
    caminho.append(caminho[0])
    return caminho # é só ir removendo os vertices que se repetem, colocando os que não se repetem em uma nova lista, ai isso vira um ciclo hamiltoniano pois você remove os ciclos com vertices

def custo_total(grafo, ciclo): # temos no final um ciclo hamiltoniano mas ele pede a soma dos pesos desse ciclo, então temos que pegar os pesos das arestas desse caminho e somar
    total = 0
    for i in range(len(ciclo) - 1): # ele vai iterar sobre a lista de vertices (o ciclo hamiltoniano)
        origem = ciclo[i] # pega o atual da iteração
        destino = ciclo[i + 1] # e pega o seguinte da iteração, ou seja, origem e destino de uma aresta
        peso = next(p for d, p in grafo[origem] if d == destino) # procura na lista de arestas de origem (na chave origem do dicionario) primeiro elemento da tupla nesse caso d, e retorna p (o peso)
        total += peso
    return total 

def christofides(): # função principal, ela só mostra um fluxo das operações, como cada algoritmo vem após o outro usando o resultado do anterior, acho que isso já é explicativo
    grafo = leitura_arquivo("grafo.txt")
    mst = prim(grafo)
    # print(mst)
    impares = vertices_impares(mst)
    # print(impares)
    aux = grafo_auxiliar(grafo, impares)
    # print(aux)
    emparelhamento = nx.algorithms.matching.min_weight_matching(aux) # função já pronta para achar o emparelhamento perfeito mínimo dos vertices impares
    # print(emparelhamento)

    for u, v in emparelhamento: # aqui você "soma" as arestas do emparelhamento com a mst para todos os vertices da mst ter grau par e ser possivel achar um ciclo euleriano com o algoritmo do hierholzer
        peso = next(p for d, p in grafo[u] if d == v)
        mst[u].append((v, peso))
        mst[v].append((u, peso))

    circuito = ciclo_euleriano(mst)
    # print(" -> ".join(map(str, circuito)))
    ciclo_final = ciclo_hamiltoniano(circuito)
    custo = custo_total(grafo, ciclo_final)

    print(" -> ".join(map(str, ciclo_final)))
    print(f"Peso total do ciclo hamiltoniano: {custo}")

if __name__ == "__main__": # você pode descomentar os print's acima para ver o fluxo do programa com mais clareza ao rodar ele se quiser, desde achar a arvore geradora, até o ciclo hamiltoriano
    christofides()