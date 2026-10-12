# Armazenar pontos  e conexões entre eles.

# Estrutura de dados que representa a rede de transporte do MetroNet.

class Grafo:
    """
    • Representa uma rede de pontos e conexões com pesos.
    • Os pontos ficam em um conjunto, pois não podem se repetir. As conexões
    ficam em um dicionário: para cada ponto, guardamos uma lista de tuplas
    no formato (vizinho, peso).
    """

    def __init__(self, direcionado=False):
        """
        • Cria um grafo vazio.
        • Em uma rede não direcionada, A -> B também cria B -> A. Esse é o
        padrão porque uma ligação comum entre duas estações pode ser usada
        nos dois sentidos.
        """
        self.direcionado = direcionado
        self.pontos = set()
        self.adjacencias = {}

    def adicionar_ponto(self, identificador):
        # Adiciona um ponto à rede e devolve True se ele for novo.
        identificador = self._validar_identificador(identificador)

        # Um conjunto impede que o mesmo ponto seja cadastrado duas vezes.
        if identificador in self.pontos:
            return False

        self.pontos.add(identificador)
        self.adjacencias[identificador] = []
        return True

    def adicionar_conexao(self, origem, destino, peso):
        # Cadastra uma conexão ponderada entre dois pontos existentes.
        origem = self._validar_identificador(origem)
        destino = self._validar_identificador(destino)
        self._validar_peso(peso)

        if origem not in self.pontos or destino not in self.pontos:
            raise ValueError("Origem e destino precisam estar cadastrados na rede.")

        if self._conexao_ja_existe(origem, destino):
            raise ValueError("A conexão informada já está cadastrada.")

        # Uma tupla agrupa os dois dados de uma ligação: vizinho e peso.
        self.adjacencias[origem].append((destino, peso))

        # Se o grafo não é direcionado, a volta também deve ser registrada.
        if not self.direcionado:
            self.adjacencias[destino].append((origem, peso))

    def possui_ponto(self, identificador):
        """Informa se um ponto pertence à rede."""
        identificador = self._validar_identificador(identificador)
        return identificador in self.pontos

    def obter_pontos(self):
        """Devolve os pontos ordenados para facilitar a consulta da rede."""
        return sorted(self.pontos)

    def obter_vizinhos(self, identificador):
        """Devolve as conexões que saem de um ponto.

        Uma nova lista é devolvida para impedir que código externo altere a
        estrutura interna do grafo por acidente.
        """
        identificador = self._validar_identificador(identificador)

        if identificador not in self.pontos:
            raise ValueError("O ponto informado não está cadastrado na rede.")

        return list(self.adjacencias[identificador])

    def quantidade_pontos(self):
        """Devolve a quantidade de pontos cadastrados."""
        return len(self.pontos)

    def quantidade_conexoes(self):
        """Devolve a quantidade de conexões cadastradas na rede."""
        quantidade = 0

        for vizinhos in self.adjacencias.values():
            quantidade += len(vizinhos)

        # Em grafos não direcionados, cada conexão foi guardada duas vezes.
        if not self.direcionado:
            return quantidade // 2

        return quantidade

    def _conexao_ja_existe(self, origem, destino):
        """Verifica se já há uma conexão de origem para destino."""
        for vizinho, peso in self.adjacencias[origem]:
            if vizinho == destino:
                return True

        return False

    def _validar_identificador(self, identificador):
        """Valida e padroniza o nome usado para identificar um ponto."""
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("O identificador do ponto deve ser um texto não vazio.")

        return identificador.strip()

    def _validar_peso(self, peso):
        """Garante um peso numérico e não negativo para Dijkstra no futuro."""
        if isinstance(peso, bool) or not isinstance(peso, (int, float)):
            raise ValueError("O peso deve ser um número.")

        if peso < 0:
            raise ValueError("O peso não pode ser negativo.")
