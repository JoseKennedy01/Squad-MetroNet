import pytest

from src.algorithms.busca_largura import busca_largura
from src.models.grafo import Grafo


def criar_grafo(*pontos):
    # Cria um grafo com os pontos informados.
    grafo = Grafo()

    for ponto in pontos:
        grafo.adicionar_ponto(ponto)

    return grafo


def test_encontra_caminho_direto():
    grafo = criar_grafo("EST01", "EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert busca_largura(grafo, "EST01", "EST02") == ["EST01", "EST02"]


def test_encontra_caminho_indireto():
    grafo = criar_grafo("EST01", "EST02", "EST03")
    grafo.adicionar_conexao("EST01", "EST02", 5)
    grafo.adicionar_conexao("EST02", "EST03", 3)

    assert busca_largura(grafo, "EST01", "EST03") == [
        "EST01",
        "EST02",
        "EST03",
    ]


def test_origem_igual_ao_destino_retorna_apenas_o_ponto():
    grafo = criar_grafo("EST01")

    assert busca_largura(grafo, "EST01", "EST01") == ["EST01"]


def test_destino_inacessivel_retorna_none():
    grafo = criar_grafo("EST01", "EST02")

    assert busca_largura(grafo, "EST01", "EST02") is None


@pytest.mark.parametrize(
    ("origem", "destino"),
    [
        ("EST99", "EST01"),
        ("EST01", "EST99"),
    ],
)
def test_ponto_inexistente_gera_value_error(origem, destino):
    grafo = criar_grafo("EST01")

    with pytest.raises(ValueError):
        busca_largura(grafo, origem, destino)


def test_respeita_o_sentido_de_grafo_direcionado():
    grafo = Grafo(direcionado=True)
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert busca_largura(grafo, "EST02", "EST01") is None


def test_bfs_minimiza_conexoes_e_ignora_os_pesos():
    grafo = criar_grafo("EST01", "EST02", "EST03")
    grafo.adicionar_conexao("EST01", "EST02", 100)
    grafo.adicionar_conexao("EST01", "EST03", 1)
    grafo.adicionar_conexao("EST03", "EST02", 1)

    # O caminho direto tem uma conexão; o caminho mais barato tem duas.
    assert busca_largura(grafo, "EST01", "EST02") == ["EST01", "EST02"]

def test_encontra_um_caminho_quando_ha_multiplas_rotas_minimas():
    grafo = criar_grafo("A", "B", "C", "D")
    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("B", "D", 1)
    grafo.adicionar_conexao("A", "C", 1)
    grafo.adicionar_conexao("C", "D", 1)

    caminho = busca_largura(grafo, "A", "D")

    # Os dois caminhos têm o mesmo número mínimo de conexões.
    assert caminho in (["A", "B", "D"], ["A", "C", "D"])


def test_encontra_caminho_em_rede_maior():
    pontos = [f"EST{i:03d}" for i in range(500)]
    grafo = criar_grafo(*pontos)

    # Forma uma rede linear com 500 pontos e 499 conexões.
    for indice in range(len(pontos) - 1):
        grafo.adicionar_conexao(pontos[indice], pontos[indice + 1], 1)

    assert busca_largura(grafo, pontos[0], pontos[-1]) == pontos

def test_termina_corretamente_em_grafo_com_ciclo():
    grafo = criar_grafo("A", "B", "C", "D")
    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("B", "C", 1)
    grafo.adicionar_conexao("C", "A", 1)
    grafo.adicionar_conexao("C", "D", 1)

    caminho = busca_largura(grafo, "A", "D")

    assert caminho == ["A", "C", "D"]
    assert len(caminho) == len(set(caminho))

def test_busca_funciona_com_identificadores_com_espacos():
    # Cria pontos cujos identificadores serão normalizados pelo Grafo.
    grafo = criar_grafo("EST01", "EST02")

    # Adiciona uma conexão entre os dois pontos.
    grafo.adicionar_conexao("EST01", "EST02", 5)

    # Verifica se a busca aceita espaços externos nos parâmetros.
    caminho = busca_largura(grafo, " EST01 ", " EST02 ")
    assert caminho == ["EST01", "EST02"]

def test_grafo_vazio_gera_value_error():
    # Cria um grafo sem nenhum ponto cadastrado.
    grafo = Grafo()

    # Verifica se a busca rejeita uma origem inexistente.
    with pytest.raises(ValueError):
        busca_largura(grafo, "EST01", "EST02")

def test_todos_os_pontos_do_caminho_possuem_conexoes_validas():
    # Cria uma rede com diferentes possibilidades de deslocamento.
    grafo = criar_grafo("A", "B", "C", "D")

    grafo.adicionar_conexao("A", "B", 4)
    grafo.adicionar_conexao("B", "D", 3)
    grafo.adicionar_conexao("A", "C", 2)
    grafo.adicionar_conexao("C", "D", 5)

    # Executa a busca entre a origem e o destino.
    caminho = busca_largura(grafo, "A", "D")

    # Verifica se a busca encontrou um caminho.
    assert caminho is not None

    # Confirma que a origem e o destino estão nas extremidades.
    assert caminho[0] == "A"
    assert caminho[-1] == "D"

    # Verifica se cada par consecutivo possui uma conexão válida.
    for indice in range(len(caminho) - 1):
        atual = caminho[indice]
        proximo = caminho[indice + 1]

        vizinhos = grafo.obter_vizinhos(atual)

        assert any(
            vizinho == proximo
            for vizinho, _peso in vizinhos
        )
