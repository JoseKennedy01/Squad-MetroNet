def busca_largura(grafo, origem, destino):
    """
    Encontra um caminho com a menor quantidade de conexões entre dois pontos.

    A BFS considera somente a quantidade de conexões, ignorando os pesos
    das arestas. Portanto, o caminho encontrado não necessariamente possui
    o menor custo total.

    Quando existem vários caminhos com a mesma quantidade de conexões,
    o resultado depende da ordem dos vizinhos retornados pelo grafo.

    Retorna:
        list: identificadores dos pontos que formam o caminho encontrado.
        None: quando os pontos existem, mas não há caminho entre eles.

    Levanta:
        ValueError: quando a origem ou o destino não estão cadastrados.

    Complexidade:
        Tempo: O(V + E), considerando lista de adjacências.
        Espaço: O(V).

        V representa a quantidade de pontos e E a quantidade de conexões.
    """

    # Verifica se a origem está cadastrada no grafo.
    if not grafo.possui_ponto(origem):
        raise ValueError(f"A origem {origem!r} não está cadastrada.")

    # Verifica se o destino está cadastrado no grafo.
    if not grafo.possui_ponto(destino):
        raise ValueError(f"O destino {destino!r} não está cadastrado.")

    # Remove espaços externos para utilizar os identificadores padronizados.
    origem = origem.strip()
    destino = destino.strip()

    # Inicializa a fila com a origem.
    fila = [origem]
    indice_fila = 0

    # Marca a origem como visitada para evitar visitas repetidas.
    visitados = {origem}

    # Armazena o ponto anterior de cada vértice para reconstruir o caminho.
    predecessores = {origem: None}

    # Percorre a fila seguindo a ordem FIFO.
    while indice_fila < len(fila):
        atual = fila[indice_fila]
        indice_fila += 1

        # Interrompe a busca quando o destino é alcançado.
        if atual == destino:
            break

        # Percorre os vizinhos do ponto atual.
        # A BFS ignora os pesos e considera somente as conexões.
        for vizinho, _peso in grafo.obter_vizinhos(atual):

            # Adiciona somente os pontos que ainda não foram visitados.
            if vizinho not in visitados:
                visitados.add(vizinho)

                # Registra de onde o vizinho foi alcançado.
                predecessores[vizinho] = atual

                # Adiciona o vizinho ao final da fila.
                fila.append(vizinho)

    # Retorna None quando o destino não foi alcançado.
    if destino not in predecessores:
        return None

    # Reconstrói o caminho partindo do destino até a origem.
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    # Inverte o caminho para apresentar a sequência origem → destino.
    caminho.reverse()
    return caminho
