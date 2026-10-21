# Armazena os pontos e as conexões entre eles.
# Representa a rede de transporte do MetroNet.

import math  # Usaremos para verificar se os pesos são números finitos.
class Grafo:
    """
    Representa uma rede de pontos e conexões com pesos.

    • Os pontos são armazenados em um conjunto, evitando duplicações.
    • As conexões são armazenadas em um dicionário de listas de tuplas.
    Cada tupla contém (vizinho, peso).
    """

    def __init__(self, direcionado=False):
        # Cria um grafo vazio.
        self.direcionado = direcionado
        self.pontos = set()
        self.adjacencias = {}

    def adicionar_ponto(self, identificador):
        # Adiciona um ponto e retorna True se ele for novo.
        identificador = self._validar_identificador(identificador)

        # O conjunto permite verificar se o ponto já existe.
        if identificador in self.pontos:
            return False

        self.pontos.add(identificador)

        # Todo ponto começa com uma lista de vizinhos vazia.
        self.adjacencias[identificador] = []

        return True

    def adicionar_conexao(self, origem, destino, peso):
        # Adiciona uma conexão entre dois pontos cadastrad# 
        origem = self._validar_identificador(origem)
        destino = self._validar_identificador(destino)

        # Validamos o peso antes de modificar o grafo.
        self._validar_peso(peso)

        # Os dois pontos precisam existir antes da conexão.
        if origem not in self.pontos or destino not in self.pontos:
            raise ValueError(
                "Origem e destino precisam estar cadastrados na rede."
            )

        # Não permitimos conectar um ponto a ele mesmo.
        if origem == destino:
            raise ValueError(
                "Não é permitido conectar um ponto a ele mesmo."
            )

        # Impede o cadastro duplicado da mesma conexão.
        if self._conexao_ja_existe(origem, destino):
            raise ValueError("A conexão informada já está cadastrada.")

        # Guarda o destino e o peso em uma tupla.
        self.adjacencias[origem].append((destino, peso))

        # Em um grafo não direcionado, a conexão funciona nos dois sentidos.
        if not self.direcionado:
            self.adjacencias[destino].append((origem, peso))

    def possui_ponto(self, identificador):
        # Informa se um ponto pertence à rede. 
        identificador = self._validar_identificador(identificador)

        return identificador in self.pontos

    def obter_pontos(self):
        # Retorna os identificadores dos pontos em ordem. 
        return sorted(self.pontos)

    def obter_vizinhos(self, identificador):
        # Retorna uma cópia da lista de vizinhos de um ponto. 
        identificador = self._validar_identificador(identificador)

        if identificador not in self.pontos:
            raise ValueError("O ponto informado não está cadastrado na rede.")

        # A cópia evita alterações acidentais na lista interna do grafo.
        return list(self.adjacencias[identificador])

    def quantidade_pontos(self):
        # Retorna a quantidade de pontos cadastrados. 
        return len(self.pontos)

    def quantidade_conexoes(self):
        # Retorna a quantidade de conexões cadastradas. 
        quantidade = 0

        # Soma as conexões registradas na lista de cada ponto.
        for vizinhos in self.adjacencias.values():
            quantidade += len(vizinhos)

        # No grafo não direcionado, cada conexão aparece duas vezes.
        if not self.direcionado:
            return quantidade // 2

        return quantidade

    def _conexao_ja_existe(self, origem, destino):
        # Verifica se já existe uma conexão de origem para destino. 
        for vizinho, peso in self.adjacencias[origem]:
            if vizinho == destino:
                return True

        return False

    def _validar_identificador(self, identificador):
        # Garante que o identificador seja um texto não vazio. 
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError(
                "O identificador do ponto deve ser um texto não vazio."
            )

        # Remove espaços extras no início e no fim do texto.
        return identificador.strip()

    def _validar_peso(self, peso):
        # Aceita pesos numéricos finitos e não negativos. 
        # Em Python, bool também é considerado um tipo de inteiro.
        if isinstance(peso, bool) or not isinstance(peso, (int, float)):
            raise ValueError("O peso deve ser um número.")

        # NaN e infinito não representam pesos válidos para nossa rede.
        # Rejeita valores float que não sejam finitos.
        if isinstance(peso, float) and not math.isfinite(peso):
            raise ValueError("O peso deve ser um número finito.")

        # Pesos negativos não são permitidos.
        if peso < 0:
            raise ValueError("O peso não pode ser negativo.")
