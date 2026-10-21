def busca_largura(grafo, origem, destino):
    """
    Encontra um caminho com o menor número de conexões entre dois pontos.

    Retorna uma lista de identificadores, ou None se os pontos forem
    válidos, mas não houver caminho entre eles.

    Levanta ValueError se a origem ou o destino não estiver cadastrado.
    """
    # O próprio Grafo também valida o tipo e o formato do identificador.
    if not grafo.possui_ponto(origem):
        raise ValueError(f"A origem {origem!r} não está cadastrada.")

    if not grafo.possui_ponto(destino):
        raise ValueError(f"O destino {destino!r} não está cadastrado.")

    # O Grafo remove espaços externos ao validar; fazemos o mesmo aqui
    # para que a busca use exatamente os identificadores armazenados.
    origem = origem.strip()
    destino = destino.strip()

    # A fila segue a regra FIFO: o primeiro ponto que entra é o primeiro
    # que será explorado.
    fila = [origem]
    indice_fila = 0

    # Marcamos um ponto como visitado quando ele entra na fila.
    # Isso impede que ciclos o adicionem repetidamente.
    visitados = {origem}

    # Guardamos de onde chegamos a cada ponto para reconstruir o caminho.
    predecessores = {origem: None}

    while indice_fila < len(fila):
        atual = fila[indice_fila]
        indice_fila += 1

        # Como a fila é explorada por níveis, o destino já foi alcançado
        # pelo caminho com menos conexões.
        if atual == destino:
            break

        # Cada vizinho vem acompanhado de um peso. A BFS não usa o peso:
        # ela conta conexões. O custo será considerado pelo Dijkstra.
        for vizinho, _peso in grafo.obter_vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                predecessores[vizinho] = atual
                fila.append(vizinho)

    # Se o destino nunca foi descoberto, não existe caminho.
    if destino not in predecessores:
        return None

    # Voltamos do destino até a origem usando os predecessores.
    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]

    # A reconstrução foi feita de trás para frente.
    caminho.reverse()
    return caminho