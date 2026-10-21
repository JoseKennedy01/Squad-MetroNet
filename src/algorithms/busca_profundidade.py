def busca_profundidade(grafo, origem, destino):
    # Encontra um caminho entre dois pontos usando DFS. 

    # Valida se a origem e o destino estão cadastrados.
    if not grafo.possui_ponto(origem):
        raise ValueError(f"A origem {origem!r} não está cadastrada.")

    if not grafo.possui_ponto(destino):
        raise ValueError(f"O destino {destino!r} não está cadastrado.")

     # Remove espaços extras antes de iniciar a busca.
    origem = origem.strip()
    destino = destino.strip()

    # Se os pontos forem iguais, o caminho contém apenas esse ponto.
    if origem == destino:
        return [origem]

    # A pilha controla quais pontos ainda serão explorados.
    pilha = [origem]

    # Marca a origem como descoberta desde o início.
    visitados = {origem}

    # Registra de onde cada ponto foi alcançado.
    predecessores = {origem: None}

    while pilha:
        atual = pilha.pop()

        # A busca termina quando o destino é encontrado.
        if atual == destino:
            break

        # A ordem invertida mantém a exploração coerente com a pilha.
        for vizinho, _peso in reversed(grafo.obter_vizinhos(atual)):
            if vizinho not in visitados:
                # Marca imediatamente para evitar entradas duplicadas.
                visitados.add(vizinho)

                # Registra o ponto anterior para reconstruir o caminho.
                predecessores[vizinho] = atual

                # Adiciona o novo ponto à pilha de exploração.
                pilha.append(vizinho)

    # Se o destino não foi descoberto, não existe caminho.
    if destino not in predecessores:
        return None

    # Reconstrói o caminho do destino até a origem.
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    # Inverte para apresentar a sequência da origem ao destino.
    caminho.reverse()
    return caminho
