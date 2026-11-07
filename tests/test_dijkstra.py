import pytest

from src.algorithms.dijkstra import dijkstra
from src.models.grafo import Grafo


def criar_grafo(*pontos, direcionado=False):
    grafo = Grafo(direcionado=direcionado)
    for ponto in pontos:
        grafo.adicionar_ponto(ponto)
    return grafo


def validar_caminho_e_custo(grafo, caminho, custo_esperado):
    """Confere que cada passo existe e que seus pesos somam o custo."""
    custo_calculado = 0
    for origem, destino in zip(caminho, caminho[1:]):
        conexoes = dict(grafo.obter_vizinhos(origem))
        assert destino in conexoes
        custo_calculado += conexoes[destino]
    assert custo_calculado == pytest.approx(custo_esperado)


def test_encontra_caminho_direto_e_custo():
    grafo = criar_grafo("A", "B")
    grafo.adicionar_conexao("A", "B", 4)

    caminho, custo = dijkstra(grafo, "A", "B")

    assert caminho == ["A", "B"]
    assert custo == 4
    validar_caminho_e_custo(grafo, caminho, custo)


def test_prefere_caminho_indireto_mais_barato_que_conexao_direta():
    grafo = criar_grafo("A", "B", "C")
    grafo.adicionar_conexao("A", "B", 10)
    grafo.adicionar_conexao("A", "C", 2)
    grafo.adicionar_conexao("C", "B", 3)

    caminho, custo = dijkstra(grafo, "A", "B")

    assert caminho == ["A", "C", "B"]
    assert custo == 5
    validar_caminho_e_custo(grafo, caminho, custo)


def test_escolhe_a_rota_de_menor_custo_entre_varias_opcoes():
    grafo = criar_grafo("A", "B", "C", "D", "E")
    grafo.adicionar_conexao("A", "B", 3)
    grafo.adicionar_conexao("B", "D", 8)
    grafo.adicionar_conexao("A", "C", 4)
    grafo.adicionar_conexao("C", "D", 2)
    grafo.adicionar_conexao("A", "E", 1)
    grafo.adicionar_conexao("E", "D", 9)

    caminho, custo = dijkstra(grafo, "A", "D")

    assert caminho == ["A", "C", "D"]
    assert custo == 6
    validar_caminho_e_custo(grafo, caminho, custo)


def test_aceita_uma_das_rotas_quando_os_custos_sao_iguais():
    grafo = criar_grafo("A", "B", "C", "D")
    grafo.adicionar_conexao("A", "B", 2)
    grafo.adicionar_conexao("B", "D", 3)
    grafo.adicionar_conexao("A", "C", 1)
    grafo.adicionar_conexao("C", "D", 4)

    caminho, custo = dijkstra(grafo, "A", "D")

    assert caminho in (["A", "B", "D"], ["A", "C", "D"])
    assert custo == 5
    validar_caminho_e_custo(grafo, caminho, custo)


def test_origem_igual_ao_destino_retorna_custo_zero():
    grafo = criar_grafo("A")

    assert dijkstra(grafo, "A", "A") == (["A"], 0)


def test_destino_inacessivel_retorna_none():
    grafo = criar_grafo("A", "B")

    assert dijkstra(grafo, "A", "B") is None


@pytest.mark.parametrize(
    ("origem", "destino"),
    [("X", "A"), ("A", "X")],
)
def test_ponto_inexistente_gera_value_error(origem, destino):
    grafo = criar_grafo("A")

    with pytest.raises(ValueError):
        dijkstra(grafo, origem, destino)


def test_respeita_direcao_das_conexoes():
    grafo = criar_grafo("A", "B", direcionado=True)
    grafo.adicionar_conexao("A", "B", 2)

    assert dijkstra(grafo, "A", "B") == (["A", "B"], 2)
    assert dijkstra(grafo, "B", "A") is None


def test_aceita_peso_zero_e_calcula_custo_total():
    grafo = criar_grafo("A", "B", "C")
    grafo.adicionar_conexao("A", "B", 0)
    grafo.adicionar_conexao("B", "C", 2.5)

    caminho, custo = dijkstra(grafo, "A", "C")

    assert caminho == ["A", "B", "C"]
    assert custo == 2.5
    validar_caminho_e_custo(grafo, caminho, custo)


def test_compara_custo_decimal_com_tolerancia_numerica():
    grafo = criar_grafo("A", "B", "C")
    grafo.adicionar_conexao("A", "B", 0.1)
    grafo.adicionar_conexao("B", "C", 0.2)

    caminho, custo = dijkstra(grafo, "A", "C")

    assert caminho == ["A", "B", "C"]
    assert custo == pytest.approx(0.3)
    validar_caminho_e_custo(grafo, caminho, 0.3)


def test_calcula_rota_em_rede_com_varias_conexoes():
    grafo = criar_grafo("A", "B", "C", "D", "E", "F")
    grafo.adicionar_conexao("A", "B", 7)
    grafo.adicionar_conexao("A", "C", 2)
    grafo.adicionar_conexao("C", "B", 1)
    grafo.adicionar_conexao("B", "D", 3)
    grafo.adicionar_conexao("C", "E", 5)
    grafo.adicionar_conexao("E", "D", 1)
    grafo.adicionar_conexao("D", "F", 4)

    caminho, custo = dijkstra(grafo, "A", "F")

    assert caminho == ["A", "C", "B", "D", "F"]
    assert custo == 10
    validar_caminho_e_custo(grafo, caminho, custo)
