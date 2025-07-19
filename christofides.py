import networkx as nx # Biblioteca usada para o emparelhamento perfeito mínimo
import heapq # Biblioteca usada para o heap mínimo em prim

def leitura_arquivo(caminho: str): # Faz a leitura e tradução do arquivo .txt para a estrutura de matriz de adjacência
    with open(caminho, 'r') as f: # Abre o arquivo enviado no modo leitura e o chama de f
        linhas = f.read().splitlines() # Armazena f em linhas dividindo ele em uma lista de linhas

    n = int(linhas[0]) # Conforme especificado na descrição do trabalho, a primeira linha é o número de vértices
    matriz = [] # Inicializa a matriz de adjacência

    for i in range(n): # Itera sobre o número de vértices - 1
        linha = list(map(float, linhas[i + 1].split())) # Somamos +1 pois a primeira linha é o número de vértices
        # Olhando de dentro para fora, cada linha é dividida onde existir espaços, transformando os valores ->
        # Em ponto flutuante por meio da função map e transformando o retorno em uma lista (cada iteração gera uma lista de floats ou seja os pesos)
        matriz.append(linha)
        # Essa lista é adicionada à matriz formando a matriz de adjacência linha por linha
    return matriz

def prim(grafo): # Algoritmo de prim para encontrar a árvore geradora mínima
    vertices = list(range(len(grafo)))  # Armazena os vértices em uma lista
    visitados = set() # Inicializa a estrutura hashset, utilizada para salvar os vértices já inseridos na árvore
    mst = {v: [] for v in vertices} # Inicializa a estrutura da árvore por meio de compressão de dicionário (chave: valor)

    inicio = vertices[0] # Usa o vértice 0 como vértice inicial
    visitados.add(inicio) # Adiciona ele para os vértices já visitados

    heap = [] # Inicializa o heap para armazenar as arestas com os menores pesos
    for destino in vertices: # Itera sobre todos os vértices do grafo completo
        if destino not in visitados: # Se não existir na árvore, adiciona a aresta ao heap que mantém a aresta de menor peso no "topo"
            # Nesse caso, todas as arestas conectadas ao vértice inicial serão adicionadas
            heapq.heappush(heap, (grafo[inicio][destino], inicio, destino))  # (peso, origem, destino)

    while heap: # Após termos os valores iniciais iniciamos o algoritmo... Enquando a pilha não for vazia, faça:
        peso, origem, destino = heapq.heappop(heap) # Remove a menor aresta do heap e armazena os respectivos valores nas variáveis
        if destino not in visitados: # Se o vértice de destino da aresta não existir na árvore, a aresta e o vértice podem ser adicionados
            visitados.add(destino) # Adiciona o novo vértice ao hashset
            mst[origem].append((destino, peso)) # Adiciona a aresta na lista de adjacência do vértice de origem
            mst[destino].append((origem, peso)) # E o mesmo para o vértice de destino para manter a simetria do grafo não direcionado
            for aresta in vertices: # Itera sobre todos os vértices do grafo completo
                    if aresta not in visitados: # Caso o vértice não exista na árvore, adicionamos as arestas do vértice destino da aresta anterior até ele
                        heapq.heappush(heap, (grafo[destino][aresta], destino, aresta))  # (peso, origem, destino)

    return mst

def vertices_impares(arvore_geradora): # Função que retornar os vértices de grau ímpar da árvore geradora mínima
    return [v for v, adj in arvore_geradora.items() if len(adj) % 2 != 0] # Faz uma compressão de lista para ->
    # retornar toda chave do dicionário (o vértice) que possui como valor uma lista com um número ímpar de elementos (a lista de adjacência do vértice)

def grafo_auxiliar(grafo, vertices): # Função que cria a estrutura aceita pela função do emparelhamento, retornando um grafo completo com o vértices de grau ímpar
    G = nx.Graph() # Inicializa a estrutura do grafo
    for u in vertices:
        for v in vertices: # Itera sobre todas as possibilidades de duplas de vértices
            peso = grafo[u][v] # Pega o peso da aresta (u, v)
            if peso > 0 and u != v: # Ignora quando os vértices forem iguais
                G.add_edge(u, v, weight=peso) # Adiciona a aresta no grafo especificando o peso (weight)
    return G # Retorna o grafo completo

def ciclo_euleriano(grafo): # Algoritmo para encontrar um ciclo euleriano dado um grafo com todos os vértices com grau par
    circuito = [] # Inicializa a estrutura que será retornada (o ciclo euleriano)
    stack = [0] # Inicia a pilha com o vértice inicial, nesse caso o 0

    while stack: # Enquanto a pilha não for vazia, faça:
        atual = stack[-1] # Pega o elemento no topo da pilha (vértice)
        if grafo[atual]: # Verifica se a chave do dicionário (vértice) armazena algum valor (lista de arestas)
            proxima = grafo[atual].pop(0) # Pega a primeira tupla, nesse caso a aresta (destino, peso) da lista de adjacência do vértice e a remove
            grafo[proxima[0]].remove((atual, proxima[1])) # Acessa a lista do vértice de destino da aresta anterior para remover a mesma aresta, mantendo a simetria
            stack.append(proxima[0]) # Adiciona o vértice de destino na pilha
        else: # Caso o vértice do topo da pilha não possua mais arestas em sua lista, faça:
            circuito.append(stack.pop()) # Remova do topo da pilha e adicione no ciclo euleriano (ou seja, o ciclo é gerado em ordem reversa)
    return circuito # Ao término do while, o ciclo é retornado

def ciclo_hamiltoniano(circuito): # Retorna o ciclo hamiltoniano com base na não repetição de vértices do ciclo euleriano
    ciclo = [] # Inicializa a futura lista de vértices
    for v in circuito: # Itera sobre cada vértice do ciclo euleriano
        if v not in ciclo: # Caso o vértice não tenha sido inserido no ciclo hamiltoniano, faça:
            ciclo.append(v) # Adicione-o
    ciclo.append(ciclo[0]) # Para fechar o ciclo, adicione o primeiro vértice do ciclo ao final da lista
    return ciclo

def custo_total(grafo, ciclo): # Recebe o grafo completo, e o ciclo hamiltoniano
    total = 0.0 # Inicializa a variável onde a soma vai ser armazenada
    for i in range(len(ciclo) - 1): # Itera do primeiro elemento do ciclo até o penúltimo (pois o acesso posterior é feito com i + 1)
        origem = ciclo[i] # O vértice atual da iteração é armazenado
        destino = ciclo[i + 1] # O vértice seguinte da iteração também é armazenado
        peso = grafo[origem][destino] # Usa-se como índices para acessar o peso da aresta referente a ele e acrescentar a soma total
        total += peso

    return total

def christofides(): # Função principal
    grafo = leitura_arquivo("lin318.txt") # Informa o nome do arquivo .txt com a matriz de adjacência para passar para a função
    mst = prim(grafo) # Encontra a árvore geradora mínima com base no grafo completo

    print("Arvore geradora minima: \n")
    print(mst)
    peso_mst = 0.0
    for v in mst.values(): # Itera sobre as listas de tuplas
        for (_, p) in v: # Itera sobre as tuplas das listas
            peso_mst += p # Soma o peso para obter o peso total da árvore geradora mínima

    print(f"\nPeso total da Arvore geradora Minima: {peso_mst / 2}\n") # Como o grafo é não direcionado os pesos são somados 2 vezes, então precisa-se dividir por 2

    impares = vertices_impares(mst) # Retorna a lista de vértices com grau ímpar da mst
    aux = grafo_auxiliar(grafo, impares) # Retorna a estrutura de grafo completa dos vértices impares aceita pela função de emparelhamento
    emparelhamento = nx.algorithms.matching.min_weight_matching(aux) # Chama a função de emparelhamento com o grafo formado pelo vértices impares

    for u, v in emparelhamento: # Adiciona as arestas de cada dupla de vértice emparelhada na mst, criando um multigrafo
        peso = grafo[u][v]
        mst[u].append((v, peso))
        mst[v].append((u, peso))

    circuito = ciclo_euleriano(mst) # Encontra um ciclo euleriano no multigrafo
    ciclo_final = ciclo_hamiltoniano(circuito) # Determina um ciclo hamiltoniano
    custo = custo_total(grafo, ciclo_final) # Retorna o custo total do ciclo hamiltoniano encontrado

    print("Solucao aproximada encontrada por Christofides: ")
    print(" -> ".join(map(str, ciclo_final))) # Transforma os valores inteiros em string e insere entre cada elemento uma seta, indicando a direção do ciclo
    print(f"\nPeso total da solucao aproximada: {custo}\n")

if __name__ == "__main__":
    christofides()