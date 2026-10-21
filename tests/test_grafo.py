# Testes automatizados da estrutura de grafo do MetroNet.

import pytest
from src.models.grafo import Grafo

def test_grafo_nasce_vazio():
    # Um grafo novo não possui pontos nem conexões. 
    grafo = Grafo()

    assert grafo.quantidade_pontos() == 0
    assert grafo.quantidade_conexoes() == 0
    assert grafo.obter_pontos() == []


def test_adicionar_ponto_guarda_apenas_uma_vez():
    # Um identificador repetido não cria outro ponto. 
    grafo = Grafo()

    assert grafo.adicionar_ponto("EST01") is True
    assert grafo.adicionar_ponto("EST01") is False

    assert grafo.quantidade_pontos() == 1
    assert grafo.possui_ponto("EST01") is True


def test_identificador_com_espacos_e_padronizado():
    # Espaços extras não criam identificadores diferentes. 
    grafo = Grafo()

    grafo.adicionar_ponto(" EST01 ")

    assert grafo.possui_ponto("EST01") is True
    assert grafo.quantidade_pontos() == 1


def test_nao_permite_identificadores_invalidos():
    # Identificadores vazios ou que não sejam textos são rejeitados. 
    grafo = Grafo()

    # Cada valor inválido deve provocar ValueError.
    for identificador in ["", "   ", 123, None]:
        with pytest.raises(ValueError):
            grafo.adicionar_ponto(identificador)


def test_adicionar_conexao_nao_direcionada_cria_dois_sentidos():
    # Uma conexão não direcionada pode ser percorrida nos dois sentidos. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert grafo.obter_vizinhos("EST01") == [("EST02", 5)]
    assert grafo.obter_vizinhos("EST02") == [("EST01", 5)]
    assert grafo.quantidade_conexoes() == 1

def test_adicionar_conexao_direcionada_cria_apenas_um_sentido():
    # Uma conexão direcionada não cria automaticamente a volta. 
    grafo = Grafo(direcionado=True)
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert grafo.obter_vizinhos("EST01") == [("EST02", 5)]
    assert grafo.obter_vizinhos("EST02") == []
    assert grafo.quantidade_conexoes() == 1

def test_nao_permite_conexao_com_ponto_nao_cadastrado():
    # Os dois extremos da conexão precisam existir. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")

    # O destino não existe.
    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST01", "EST02", 5)

    # A origem não existe.
    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST02", "EST01", 5)

def test_nao_permite_conectar_ponto_a_ele_mesmo():
    # Uma conexão não pode ter a mesma origem e destino. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")

    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST01", "EST01", 5)

    # A operação inválida não deve alterar a quantidade de conexões.
    assert grafo.quantidade_conexoes() == 0
    assert grafo.obter_vizinhos("EST01") == []

def test_nao_permite_pesos_invalidos():
    # Pesos negativos, textos, booleanos e valores não finitos são rejeitados. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    pesos_invalidos = [
        -1,
        "cinco",
        True,
        float("nan"),
        float("inf"),
        float("-inf"),
    ]

    for peso in pesos_invalidos:
        with pytest.raises(ValueError):
            grafo.adicionar_conexao("EST01", "EST02", peso)

def test_permite_peso_zero_e_decimal():
    # Pesos zero e decimais são válidos. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_ponto("EST03")

    grafo.adicionar_conexao("EST01", "EST02", 0)
    grafo.adicionar_conexao("EST02", "EST03", 2.5)

    assert grafo.obter_vizinhos("EST01") == [("EST02", 0)]
    assert grafo.obter_vizinhos("EST02") == [
        ("EST01", 0),
        ("EST03", 2.5),
    ]
    assert grafo.quantidade_conexoes() == 2

def test_nao_permite_conexao_repetida():
    # A mesma conexão não pode ser cadastrada duas vezes. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST01", "EST02", 5)

    assert grafo.quantidade_conexoes() == 1

def test_nao_permite_conexao_repetida_no_sentido_inverso():
    # A conexão inversa também é duplicada em um grafo não direcionado. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST02", "EST01", 5)

    assert grafo.quantidade_conexoes() == 1

def test_nao_permite_consultar_vizinhos_de_ponto_inexistente():
    # A consulta deve rejeitar um ponto que não foi cadastrado. 
    grafo = Grafo()

    with pytest.raises(ValueError):
        grafo.obter_vizinhos("EST99")

def test_obter_pontos_retorna_lista_ordenada():
    # A consulta de pontos deve retornar os identificadores ordenados. 
    grafo = Grafo()

    grafo.adicionar_ponto("EST03")
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    assert grafo.obter_pontos() == ["EST01", "EST02", "EST03"]

def test_quantidade_de_conexoes_com_varios_pontos():
    # A quantidade deve corresponder às conexões realmente cadastradas. 
    grafo = Grafo()

    for identificador in ["EST01", "EST02", "EST03", "EST04"]:
        grafo.adicionar_ponto(identificador)

    grafo.adicionar_conexao("EST01", "EST02", 5)
    grafo.adicionar_conexao("EST02", "EST03", 3)
    grafo.adicionar_conexao("EST03", "EST04", 7)

    assert grafo.quantidade_pontos() == 4
    assert grafo.quantidade_conexoes() == 3

def test_copia_da_lista_de_vizinhos_nao_altera_o_grafo():
    # Alterar a lista retornada não modifica as adjacências internas. 
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    vizinhos = grafo.obter_vizinhos("EST01")

    # Removemos um elemento apenas da cópia devolvida pelo método.
    vizinhos.clear()

    # A conexão original continua armazenada no grafo.
    assert grafo.obter_vizinhos("EST01") == [("EST02", 5)]
