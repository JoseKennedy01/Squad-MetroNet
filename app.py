"""API local do MetroNet para a demonstração web."""

from pathlib import Path
from threading import RLock

from flask import Flask, jsonify, request, send_from_directory

from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra
from src.models.grafo import Grafo


BASE_DIR = Path(__file__).resolve().parent
LOCK = RLock()

ESTACOES_DEMO = [
    {"id": "EST01", "nome": "Terminal", "tipo": "metro"},
    {"id": "EST02", "nome": "Museu", "tipo": "metro"},
    {"id": "EST03", "nome": "Universidade", "tipo": "metro"},
    {"id": "EST04", "nome": "Centro", "tipo": "metro"},
    {"id": "EST05", "nome": "Mercado", "tipo": "metro"},
    {"id": "EST06", "nome": "Hospital", "tipo": "metro"},
    {"id": "EST07", "nome": "Parque", "tipo": "metro"},
    {"id": "EST08", "nome": "Aeroporto", "tipo": "metro"},
    {"id": "EST09", "nome": "Rodoviária", "tipo": "metro"},
]

CONEXOES_DEMO = [
    ("EST01", "EST04", 5),
    ("EST04", "EST07", 4),
    ("EST07", "EST09", 5),
    ("EST01", "EST02", 10),
    ("EST02", "EST09", 10),
    ("EST04", "EST05", 3),
    ("EST05", "EST06", 2),
    ("EST06", "EST08", 2),
    ("EST08", "EST09", 6),
]


def criar_rede_demo():
    rede = Grafo(direcionado=False)
    metadados = {}
    for estacao in ESTACOES_DEMO:
        rede.adicionar_ponto(estacao["id"])
        metadados[estacao["id"]] = {
            **estacao,
            "personalizada": False,
        }
    for origem, destino, peso in CONEXOES_DEMO:
        rede.adicionar_conexao(origem, destino, peso)
    return rede, metadados


grafo, estacoes = criar_rede_demo()
app = Flask(__name__, static_folder=None)


def erro(mensagem, status=400):
    return jsonify({"erro": str(mensagem)}), status


def custo_do_caminho(caminho):
    if not caminho:
        return None
    total = 0
    for origem, destino in zip(caminho, caminho[1:]):
        pesos = dict(grafo.obter_vizinhos(origem))
        total += pesos[destino]
    return total


@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")


@app.get("/app.js")
def javascript():
    return send_from_directory(BASE_DIR, "app.js")


@app.get("/estacoes")
def listar_estacoes():
    with LOCK:
        resultado = [estacoes[ponto] for ponto in grafo.obter_pontos()]
        return jsonify({"estacoes": resultado})


@app.post("/estacoes")
def adicionar_estacao():
    global grafo
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro('O corpo da requisição deve ser um objeto JSON.')
    nome = dados.get("nome")
    tipo = str(dados.get("tipo", "metro")).strip().lower()
    if not isinstance(nome, str) or not nome.strip():
        return erro("Informe o nome da estação.")
    if tipo not in {"metro", "carro"}:
        return erro("A modalidade deve ser 'metro' ou 'carro'.")

    prefixo = "CARRO" if tipo == "carro" else "METRO"
    with LOCK:
        numero = 1
        identificador = f"{prefixo}{numero:02d}"
        while grafo.possui_ponto(identificador):
            numero += 1
            identificador = f"{prefixo}{numero:02d}"
        try:
            grafo.adicionar_ponto(identificador)
        except ValueError as exc:
            return erro(exc)
        estacoes[identificador] = {
            "id": identificador,
            "nome": nome.strip(),
            "tipo": tipo,
            "personalizada": True,
        }
        return jsonify({"estacao": estacoes[identificador]}), 201


@app.delete("/estacoes/<identificador>")
def remover_estacao(identificador):
    with LOCK:
        if identificador not in estacoes:
            return erro("A estação informada não está cadastrada.", 404)
        if not estacoes[identificador]["personalizada"]:
            return erro("As estações do exemplo não podem ser removidas.", 409)
        try:
            grafo.remover_ponto(identificador)
        except ValueError as exc:
            return erro(exc, 404)
        del estacoes[identificador]
        return "", 204


@app.get("/conexoes")
def listar_conexoes():
    with LOCK:
        conexoes = [
            {"origem": origem, "destino": destino, "peso": peso}
            for origem, destino, peso in grafo.obter_conexoes()
        ]
        return jsonify({"conexoes": conexoes})


@app.post("/conexoes")
def adicionar_conexao():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro('O corpo da requisição deve ser um objeto JSON.')
    origem = dados.get("origem")
    destino = dados.get("destino")
    peso = dados.get("peso")
    with LOCK:
        try:
            grafo.adicionar_conexao(origem, destino, peso)
        except (ValueError, TypeError) as exc:
            return erro(exc)
        return jsonify({"origem": origem, "destino": destino, "peso": peso}), 201


@app.delete("/conexoes")
def remover_conexao():
    origem = request.args.get("origem", "")
    destino = request.args.get("destino", "")
    with LOCK:
        try:
            grafo.remover_conexao(origem, destino)
        except ValueError as exc:
            status = 404 if "não está cadastrada" in str(exc) else 400
            return erro(exc, status)
        return "", 204


@app.get("/rota")
def consultar_rota():
    origem = request.args.get("origem", "")
    destino = request.args.get("destino", "")
    algoritmo = request.args.get("algoritmo", "dijkstra").strip().lower()
    if algoritmo not in {"bfs", "dfs", "dijkstra"}:
        return erro("Algoritmo inválido. Use bfs, dfs ou dijkstra.")

    with LOCK:
        try:
            if algoritmo == "bfs":
                caminho, visitados = busca_largura(grafo, origem, destino, retornar_visitados=True)
                custo = custo_do_caminho(caminho)
            elif algoritmo == "dfs":
                caminho, visitados = busca_profundidade(grafo, origem, destino, retornar_visitados=True)
                custo = custo_do_caminho(caminho)
            else:
                caminho, custo, visitados = dijkstra(grafo, origem, destino, retornar_visitados=True)
        except ValueError as exc:
            return erro(exc)

    return jsonify({
        "algoritmo": algoritmo,
        "origem": origem.strip(),
        "destino": destino.strip(),
        "caminho": caminho,
        "custo": custo,
        "conexoes": len(caminho) - 1 if caminho is not None else None,
        "visitados": visitados,
    })


@app.post("/rede/restaurar")
def restaurar_rede_demo():
    global grafo, estacoes
    with LOCK:
        grafo, estacoes = criar_rede_demo()
    return jsonify({"mensagem": "Rede de demonstração restaurada."})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
