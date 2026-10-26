import csv
import pytest
from src.data.carregar_rede import carregar_rede
from src.data.gerar_rede_sintetica import gerar_rede_sintetica

def criar_csv(caminho, linhas):
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["origem", "destino", "peso"])
        escritor.writerows(linhas)


def test_carrega_rede_nao_direcionada(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(
        caminho,
        [
            ["A", "B", "2.5"],
            ["B", "C", "1"],
        ],
    )

    grafo = carregar_rede(caminho)

    assert grafo.direcionado is False
    assert grafo.obter_pontos() == ["A", "B", "C"]
    assert grafo.quantidade_conexoes() == 2
    assert grafo.obter_vizinhos("A") == [("B", 2.5)]
    assert grafo.obter_vizinhos("B") == [("A", 2.5), ("C", 1.0)]

def test_rejeita_conexao_duplicada(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "B", "2"], ["B", "A", "2"]])

    with pytest.raises(ValueError, match="conexão inválida"):
        carregar_rede(caminho)

def test_rejeita_peso_negativo(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "B", "-1"]])

    with pytest.raises(ValueError, match="conexão inválida"):
        carregar_rede(caminho)

def test_rejeita_campo_vazio(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "", "2"]])

    with pytest.raises(ValueError, match="campos não podem ficar vazios"):
        carregar_rede(caminho)

def test_rejeita_csv_sem_conexoes(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [])

    with pytest.raises(ValueError, match="não possui conexões"):
        carregar_rede(caminho)

def test_rejeita_arquivo_inexistente(tmp_path):
    caminho = tmp_path / "inexistente.csv"

    with pytest.raises(FileNotFoundError):
        carregar_rede(caminho)

def test_rejeita_cabecalho_invalido(tmp_path):
    caminho = tmp_path / "rede.csv"
    caminho.write_text(
        "origem,destino,distancia\nA,B,2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="cabeçalho"):
        carregar_rede(caminho)

def test_rejeita_peso_nao_numerico(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "B", "abc"]])

    with pytest.raises(ValueError, match="peso deve ser numérico"):
        carregar_rede(caminho)

@pytest.mark.parametrize("peso", ["inf", "-inf", "nan"])
def test_rejeita_pesos_nao_finitos(tmp_path, peso):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "B", peso]])

    with pytest.raises(ValueError, match="peso deve ser finito"):
        carregar_rede(caminho)

def test_rejeita_conexao_de_um_ponto_para_ele_mesmo(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "A", "2"]])

    with pytest.raises(ValueError, match="origem e destino são iguais"):
        carregar_rede(caminho)

def test_rejeita_colunas_extras(tmp_path):
    caminho = tmp_path / "rede.csv"
    caminho.write_text(
        "origem,destino,peso\nA,B,2,extra\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="colunas extras"):
        carregar_rede(caminho)

def test_aceita_peso_zero(tmp_path):
    caminho = tmp_path / "rede.csv"
    criar_csv(caminho, [["A", "B", "0"]])

    grafo = carregar_rede(caminho)

    assert grafo.obter_vizinhos("A") == [("B", 0.0)]
    assert grafo.obter_vizinhos("B") == [("A", 0.0)]

def test_carrega_csv_com_bom_utf8(tmp_path):
    caminho = tmp_path / "rede.csv"
    caminho.write_text(
        "\ufefforigem,destino,peso\nA,B,2\n",
        encoding="utf-8",
    )

    grafo = carregar_rede(caminho)

    assert grafo.quantidade_pontos() == 2
    assert grafo.quantidade_conexoes() == 1
    assert grafo.obter_vizinhos("A") == [("B", 2.0)]

def test_rejeita_cabecalho_com_colunas_fora_da_ordem(tmp_path):
    caminho = tmp_path / "rede.csv"
    caminho.write_text(
        "destino,origem,peso\nB,A,2\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="cabeçalho"):
        carregar_rede(caminho)

@pytest.mark.parametrize("quantidade", [0, -1, -10, 1.5, "5", True])
def test_rejeita_quantidade_de_pontos_invalida(quantidade):
    with pytest.raises(ValueError, match="inteiro positivo"):
        gerar_rede_sintetica(quantidade)

def test_gera_rede_com_um_ponto():
    grafo = gerar_rede_sintetica(1)

    assert grafo.direcionado is False
    assert grafo.obter_pontos() == ["EST001"]
    assert grafo.quantidade_conexoes() == 0

def test_gera_rede_conectada_com_varios_pontos():
    grafo = gerar_rede_sintetica(5)

    assert grafo.quantidade_pontos() == 5
    assert grafo.quantidade_conexoes() == 7

    for ponto in grafo.obter_pontos():
        assert grafo.obter_vizinhos(ponto)

def test_geracao_repetida_produz_a_mesma_rede():
    primeira = gerar_rede_sintetica(6)
    segunda = gerar_rede_sintetica(6)

    assert primeira.obter_pontos() == segunda.obter_pontos()

    for ponto in primeira.obter_pontos():
        assert primeira.obter_vizinhos(ponto) == segunda.obter_vizinhos(ponto)

def test_gera_rede_com_dois_pontos():
    grafo = gerar_rede_sintetica(2)

    assert grafo.obter_pontos() == ["EST001", "EST002"]
    assert grafo.quantidade_conexoes() == 1
    assert grafo.obter_vizinhos("EST001") == [("EST002", 1.0)]
