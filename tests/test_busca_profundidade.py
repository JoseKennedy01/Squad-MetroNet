import pytest

from src.models.grafo import Grafo
from src.algorithms.busca_profundidade import busca_profundidade


def criar_grafo_simples():
    # Cria uma rede pequena para os testes da DFS. 
    grafo = Grafo()

    for ponto in ["A", "B", "C", "D"]:
        grafo.adicionar_ponto(ponto)

    grafo.adicionar_conexao("A", "B", 5)
    grafo.adicionar_conexao("B", "C", 3)
    grafo.adicionar_conexao("A", "D", 2)

    return grafo


def validar_caminho(grafo, caminho, origem, destino):
    # Verifica se o caminho retornado corresponde a conexões reais. 

    # Um caminho válido deve começar na origem e terminar no destino.
    assert caminho[0] == origem
    assert caminho[-1] == destino

    # Cada par consecutivo precisa ter uma conexão no grafo.
    for atual, proximo in zip(caminho, caminho[1:]):
        vizinhos = {
            ponto for ponto, _peso in grafo.obter_vizinhos(atual)
        }
        assert proximo in vizinhos

def test_encontra_caminho_direto():
    grafo = criar_grafo_simples()

    caminho = busca_profundidade(grafo, "A", "D")

    assert caminho == ["A", "D"]

def test_encontra_caminho_indireto():
    grafo = criar_grafo_simples()

    caminho = busca_profundidade(grafo, "A", "C")

    assert caminho == ["A", "B", "C"]

def test_origem_igual_ao_destino():
    grafo = criar_grafo_simples()

    caminho = busca_profundidade(grafo, "A", "A")

    assert caminho == ["A"]

def test_retorna_none_quando_nao_existe_caminho():
    grafo = Grafo(direcionado=True)
    grafo.adicionar_ponto("A")
    grafo.adicionar_ponto("B")

    caminho = busca_profundidade(grafo, "A", "B")

    assert caminho is None

def test_origem_inexistente_gera_erro():
    grafo = criar_grafo_simples()

    with pytest.raises(ValueError):
        busca_profundidade(grafo, "X", "A")

def test_destino_inexistente_gera_erro():
    grafo = criar_grafo_simples()

    with pytest.raises(ValueError):
        busca_profundidade(grafo, "A", "X")

def test_respeita_direcao_das_conexoes():
    grafo = Grafo(direcionado=True)
    grafo.adicionar_ponto("A")
    grafo.adicionar_ponto("B")
    grafo.adicionar_conexao("A", "B", 4)

    assert busca_profundidade(grafo, "A", "B") == ["A", "B"]
    assert busca_profundidade(grafo, "B", "A") is None

def test_termina_corretamente_em_grafo_com_ciclo():
    grafo = Grafo()

    for ponto in ["A", "B", "C", "D"]:
        grafo.adicionar_ponto(ponto)

    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("B", "C", 1)
    grafo.adicionar_conexao("C", "A", 1)
    grafo.adicionar_conexao("C", "D", 1)

    caminho = busca_profundidade(grafo, "A", "D")

    assert caminho is not None
    assert caminho[0] == "A"
    assert caminho[-1] == "D"
    assert len(caminho) == len(set(caminho))

def test_grafo_vazio_gera_erro_para_origem_inexistente():
    grafo = Grafo()

    with pytest.raises(ValueError):
        busca_profundidade(grafo, "A", "B")

def test_ponto_isolado_nao_alcanca_outro_ponto():
    grafo = Grafo()

    grafo.adicionar_ponto("A")
    grafo.adicionar_ponto("B")
    grafo.adicionar_ponto("C")
    grafo.adicionar_conexao("A", "B", 1)

    caminho = busca_profundidade(grafo, "A", "C")

    assert caminho is None

def test_encontra_caminho_em_grafo_com_ramificacoes():
    grafo = Grafo()

    for ponto in ["A", "B", "C", "D", "E", "F"]:
        grafo.adicionar_ponto(ponto)

    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("A", "C", 1)
    grafo.adicionar_conexao("B", "D", 1)
    grafo.adicionar_conexao("C", "E", 1)
    grafo.adicionar_conexao("E", "F", 1)

    caminho = busca_profundidade(grafo, "A", "F")

    assert caminho is not None
    validar_caminho(grafo, caminho, "A", "F")

def test_caminho_retornado_contem_somente_conexoes_existentes():
    grafo = criar_grafo_simples()

    caminho = busca_profundidade(grafo, "A", "C")

    assert caminho is not None
    validar_caminho(grafo, caminho, "A", "C")


def test_identificadores_com_espacos_sao_padronizados():
    grafo = criar_grafo_simples()

    # A classe Grafo remove os espaços externos dos identificadores.
    caminho = busca_profundidade(grafo, " A ", " C ")

    # O caminho deve usar os identificadores padronizados.
    assert caminho == ["A", "B", "C"]


def test_dfs_nao_garante_o_caminho_com_menos_conexoes():
    grafo = Grafo()

    for ponto in ["S", "A", "B", "X", "T"]:
        grafo.adicionar_ponto(ponto)

    # A DFS explora primeiro o ramo longo; existe também S -> X -> T.
    grafo.adicionar_conexao("S", "A", 1)
    grafo.adicionar_conexao("S", "X", 1)
    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("B", "T", 1)
    grafo.adicionar_conexao("X", "T", 1)

    caminho = busca_profundidade(grafo, "S", "T")

    assert caminho == ["S", "A", "B", "T"]
    assert len(caminho) - 1 > 2  # A rota S -> X -> T tem duas conexões.
    validar_caminho(grafo, caminho, "S", "T")

def test_grafo_com_um_unico_ponto_retorna_o_proprio_ponto():
    # Cria um grafo contendo somente um ponto.
    grafo = Grafo()
    grafo.adicionar_ponto("A")

    # Verifica se a busca retorna o ponto quando origem e destino são iguais.
    assert busca_profundidade(grafo, "A", "A") == ["A"]

def test_encontra_destino_em_grafo_com_ciclos_e_ramificacoes():
    # Cria um grafo com diferentes caminhos, ciclos e ramificações.
    grafo = Grafo()

    for ponto in ["A", "B", "C", "D", "E", "F", "G"]:
        grafo.adicionar_ponto(ponto)

    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("A", "C", 1)
    grafo.adicionar_conexao("B", "D", 1)
    grafo.adicionar_conexao("D", "A", 1)
    grafo.adicionar_conexao("C", "E", 1)
    grafo.adicionar_conexao("E", "F", 1)
    grafo.adicionar_conexao("F", "C", 1)
    grafo.adicionar_conexao("F", "G", 1)

    # Executa a busca entre a origem e o destino.
    caminho = busca_profundidade(grafo, "A", "G")

    # Verifica se o caminho encontrado é válido e não possui repetições.
    assert caminho is not None
    validar_caminho(grafo, caminho, "A", "G")
    assert len(caminho) == len(set(caminho))

def test_caminho_em_grafo_direcionado_respeita_todas_as_conexoes():
    # Cria uma rede direcionada.
    grafo = Grafo(direcionado=True)

    for ponto in ["A", "B", "C"]:
        grafo.adicionar_ponto(ponto)

    # Adiciona conexões somente no sentido indicado.
    grafo.adicionar_conexao("A", "B", 1)
    grafo.adicionar_conexao("B", "C", 1)

    # Busca um caminho respeitando o sentido das conexões.
    caminho = busca_profundidade(grafo, "A", "C")

    assert caminho == ["A", "B", "C"]
    validar_caminho(grafo, caminho, "A", "C")

    # A busca no sentido contrário não pode encontrar um caminho.
    assert busca_profundidade(grafo, "C", "A") is None
