"""Testes da estrutura de grafo usada pelo MetroNet."""

import pytest

from src.models.grafo import Grafo

def test_grafo_nasce_vazio():
    grafo = Grafo()

    assert grafo.quantidade_pontos() == 0
    assert grafo.quantidade_conexoes() == 0
    assert grafo.obter_pontos() == []


def test_adicionar_ponto_guarda_apenas_uma_vez():
    grafo = Grafo()

    assert grafo.adicionar_ponto("EST01") is True
    assert grafo.adicionar_ponto("EST01") is False
    assert grafo.quantidade_pontos() == 1
    assert grafo.possui_ponto("EST01") is True


def test_adicionar_conexao_nao_direcionada_cria_dois_sentidos():
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert grafo.obter_vizinhos("EST01") == [("EST02", 5)]
    assert grafo.obter_vizinhos("EST02") == [("EST01", 5)]
    assert grafo.quantidade_conexoes() == 1


def test_adicionar_conexao_direcionada_cria_apenas_um_sentido():
    grafo = Grafo(direcionado=True)
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    grafo.adicionar_conexao("EST01", "EST02", 5)

    assert grafo.obter_vizinhos("EST01") == [("EST02", 5)]
    assert grafo.obter_vizinhos("EST02") == []
    assert grafo.quantidade_conexoes() == 1


def test_nao_permite_conexao_com_ponto_nao_cadastrado():
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")

    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST01", "EST02", 5)


def test_nao_permite_pesos_invalidos():
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")

    # O mesmo teste percorre uma pequena lista de valores inválidos.
    for peso_invalido in [-1, "cinco", True]:
        with pytest.raises(ValueError):
            grafo.adicionar_conexao("EST01", "EST02", peso_invalido)


def test_nao_permite_conexao_repetida():
    grafo = Grafo()
    grafo.adicionar_ponto("EST01")
    grafo.adicionar_ponto("EST02")
    grafo.adicionar_conexao("EST01", "EST02", 5)

    with pytest.raises(ValueError):
        grafo.adicionar_conexao("EST01", "EST02", 5)
