import pytest

from src.models.grafo import Grafo
from src.services.roteador import (
    executar_rota,
    obter_algoritmos_disponiveis,
)


def criar_grafo(*pontos, direcionado=False):
    grafo = Grafo(direcionado=direcionado)

    for ponto in pontos:
        grafo.adicionar_ponto(ponto)

    return grafo


def validar_caminho_e_custo(grafo, caminho, custo_esperado):
    custo_calculado = 0

    for origem, destino in zip(caminho, caminho[1:]):
        conexoes = dict(grafo.obter_vizinhos(origem))
        assert destino in conexoes
        custo_calculado += conexoes[destino]

    assert custo_calculado == pytest.approx(custo_esperado)


def test_disponibiliza_os_tres_algoritmos():
    assert obter_algoritmos_disponiveis() == ("BFS", "DFS", "DIJKSTRA")


@pytest.mark.parametrize("algoritmo", ["BFS", "DFS", "DIJKSTRA"])
def test_encontra_caminho_em_rede_simples(algoritmo):
    grafo = criar_grafo("A", "B", "C")
    grafo.adicionar_conexao("A", "B", 2)
    grafo.adicionar_conexao("B", "C", 3)

    resultado = executar_rota(grafo, "A", "C", algoritmo)

    assert resultado == (["A", "B", "C"], 5)
    validar_caminho_e_custo(grafo, resultado[0], resultado[1])


def test_dijkstra_escolhe_a_rota_de_menor_custo():
    grafo = criar_grafo("A", "B", "C")
    grafo.adicionar_conexao("A", "B", 10)
    grafo.adicionar_conexao("A", "C", 2)
    grafo.adicionar_conexao("C", "B", 3)

    caminho, custo = executar_rota(grafo, "A", "B", "DIJKSTRA")

    assert caminho == ["A", "C", "B"]
    assert custo == 5
    validar_caminho_e_custo(grafo, caminho, custo)


@pytest.mark.parametrize("algoritmo", ["BFS", "DFS", "DIJKSTRA"])
def test_retorna_none_quando_nao_existe_caminho(algoritmo):
    grafo = criar_grafo("A", "B", direcionado=True)

    assert executar_rota(grafo, "A", "B", algoritmo) is None


@pytest.mark.parametrize("algoritmo", ["BFS", "DFS", "DIJKSTRA"])
def test_origem_igual_ao_destino_tem_custo_zero(algoritmo):
    grafo = criar_grafo("A")

    assert executar_rota(grafo, "A", "A", algoritmo) == (["A"], 0)


def test_rejeita_algoritmo_invalido():
    grafo = criar_grafo("A")

    with pytest.raises(ValueError, match="Algoritmo inválido"):
        executar_rota(grafo, "A", "A", "OUTRO")