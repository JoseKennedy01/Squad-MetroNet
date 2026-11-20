import pytest

import app as metro


@pytest.fixture
def client():
    metro.app.config.update(TESTING=True)
    with metro.app.test_client() as test_client:
        test_client.post("/rede/restaurar")
        yield test_client
        test_client.post("/rede/restaurar")


def test_aplicacao_serve_interface_e_ativos(client):
    assert client.get("/").status_code == 200
    assert client.get("/style.css").status_code == 200
    assert client.get("/app.js").status_code == 200


@pytest.mark.parametrize(
    ("algoritmo", "caminho", "custo", "conexoes"),
    [
        ("bfs", ["EST01", "EST02", "EST09"], 20, 2),
        ("dfs", ["EST01", "EST04", "EST07", "EST09"], 14, 3),
        ("dijkstra", ["EST01", "EST04", "EST07", "EST09"], 14, 3),
    ],
)
def test_rota_retorna_caminho_custo_e_quantidade_de_conexoes(
    client, algoritmo, caminho, custo, conexoes
):
    resposta = client.get(
        "/rota",
        query_string={
            "origem": "EST01",
            "destino": "EST09",
            "algoritmo": algoritmo,
        },
    )

    assert resposta.status_code == 200
    assert resposta.json["caminho"] == caminho
    assert resposta.json["custo"] == custo
    assert resposta.json["conexoes"] == conexoes


@pytest.mark.parametrize("endpoint", ["/estacoes", "/conexoes"])
def test_post_rejeita_json_que_nao_seja_objeto(client, endpoint):
    resposta = client.post(endpoint, json=["campo", "invalido"])

    assert resposta.status_code == 400
    assert resposta.json["erro"]


def test_rota_sem_caminho_retorna_conexoes_nulas(client):
    estacao = client.post("/estacoes", json={"nome": "Ilha", "tipo": "metro"})
    destino = estacao.json["estacao"]["id"]

    resposta = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": destino, "algoritmo": "dijkstra"},
    )

    assert resposta.status_code == 200
    assert resposta.json["caminho"] is None
    assert resposta.json["custo"] is None
    assert resposta.json["conexoes"] is None


def test_est01_alcanca_est05_na_rede_de_demonstracao(client):
    resposta = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": "EST05", "algoritmo": "bfs"},
    )

    assert resposta.status_code == 200
    assert resposta.json["caminho"] == ["EST01", "EST04", "EST05"]
    assert resposta.json["custo"] == 8
    assert resposta.json["conexoes"] == 2

def test_cenario_pdf_informa_ausencia_de_rota_para_est03(client):
    resposta = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": "EST03", "algoritmo": "dijkstra"},
    )

    assert resposta.status_code == 200
    assert resposta.json["caminho"] is None
    assert resposta.json["custo"] is None
    assert resposta.json["conexoes"] is None

def test_rota_da_estacao_para_ela_mesma_tem_zero_conexoes(client):
    resposta = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": "EST01", "algoritmo": "dijkstra"},
    )

    assert resposta.status_code == 200
    assert resposta.json["caminho"] == ["EST01"]
    assert resposta.json["custo"] == 0
    assert resposta.json["conexoes"] == 0


def test_crud_de_estacao_e_conexao_na_api(client):
    estacao = client.post("/estacoes", json={"nome": "Estação nova", "tipo": "carro"})
    assert estacao.status_code == 201
    identificador = estacao.json["estacao"]["id"]

    conexao = client.post(
        "/conexoes",
        json={"origem": "EST01", "destino": identificador, "peso": 2},
    )
    assert conexao.status_code == 201
    assert conexao.json == {"origem": "EST01", "destino": identificador, "peso": 2}

    rota = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": identificador, "algoritmo": "dijkstra"},
    )
    assert rota.json["caminho"] == ["EST01", identificador]
    assert rota.json["conexoes"] == 1
    assert rota.json["custo"] == 2

    removida = client.delete(f"/estacoes/{identificador}")
    assert removida.status_code == 204
    assert len(client.get("/conexoes").json["conexoes"]) == 9


def test_api_retorna_400_para_algoritmo_e_estacao_invalidos(client):
    algoritmo = client.get(
        "/rota",
        query_string={"origem": "EST01", "destino": "EST09", "algoritmo": "invalido"},
    )
    estacao = client.get(
        "/rota",
        query_string={"origem": "DESCONHECIDA", "destino": "EST09"},
    )

    assert algoritmo.status_code == 400
    assert estacao.status_code == 400
    assert algoritmo.json["erro"]
    assert estacao.json["erro"]