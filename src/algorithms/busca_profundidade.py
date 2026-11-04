def busca_profundidade(grafo, origem, destino):
    """
    Encontra um caminho entre dois pontos utilizando busca em profundidade.

    A DFS explora um caminho até onde consegue antes de retornar e explorar
    outras possibilidades. Por isso, não garante o caminho com a menor
    quantidade de conexões nem o menor custo total.

    Quando existem vários caminhos possíveis, o resultado depende da ordem
    dos vizinhos retornados pelo grafo.

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

    # Remove espaços externos dos identificadores.
    origem = origem.strip()
    destino = destino.strip()

    # Se origem e destino forem iguais, retorna somente esse ponto.
    if origem == destino:
        return [origem]

    # Inicializa a pilha com o ponto de origem.
    pilha = [origem]

    # Marca a origem como visitada para evitar visitas repetidas.
    visitados = {origem}

    # Armazena o ponto anterior de cada vértice.
    predecessores = {origem: None}

    # Continua enquanto existirem pontos para explorar.
    while pilha:
        # Remove o último ponto adicionado à pilha (LIFO).
        atual = pilha.pop()

        # Interrompe a busca quando o destino é encontrado.
        if atual == destino:
            break

        # Percorre os vizinhos em ordem inversa para controlar
        # a sequência de exploração da pilha.
        for vizinho, _peso in reversed(grafo.obter_vizinhos(atual)):

            # Explora somente pontos que ainda não foram visitados.
            if vizinho not in visitados:
                visitados.add(vizinho)

                # Registra de onde o vizinho foi alcançado.
                predecessores[vizinho] = atual

                # Adiciona o vizinho à pilha.
                pilha.append(vizinho)

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
