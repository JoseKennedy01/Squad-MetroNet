"""Interface de terminal para interagir com a rede MetroNet."""

from src.models.grafo import Grafo
from src.services.roteador import executar_rota, obter_algoritmos_disponiveis
from src.utils.entrada_cli import converter_peso


def exibir_rede(grafo):
    # Mostra os pontos cadastrados e suas conexões.
    pontos = grafo.obter_pontos()
    if not pontos:
        print("A rede ainda não possui pontos cadastrados.")
        return

    print("\nPontos e conexões cadastrados:")
    for ponto in pontos:
        vizinhos = grafo.obter_vizinhos(ponto)
        if vizinhos:
            conexoes = ", ".join(
                f"{vizinho} (peso {peso})" for vizinho, peso in vizinhos
            )
            print(f"- {ponto}: {conexoes}")
        else:
            print(f"- {ponto}: sem conexões")


def cadastrar_ponto(grafo):
    # Lê um identificador e solicita o cadastro ao grafo.
    identificador = input("Identificador do ponto: ")
    try:
        if grafo.adicionar_ponto(identificador):
            print("Ponto cadastrado.")
        else:
            print("Esse ponto já está cadastrado.")
    except ValueError as erro:
        print(f"Não foi possível cadastrar o ponto: {erro}")


def cadastrar_conexao(grafo):
    # Lê os dados de uma conexão e solicita seu cadastro ao grafo.
    origem = input("Ponto de origem: ")
    destino = input("Ponto de destino: ")

    try:
        peso = converter_peso(input("Peso da conexão: "))
        grafo.adicionar_conexao(origem, destino, peso)
        print("Conexão cadastrada nos dois sentidos.")
    except ValueError as erro:
        print(f"Não foi possível cadastrar a conexão: {erro}")


def buscar_rota(grafo):
    # Solicita origem, destino e algoritmo e apresenta o resultado.
    algoritmos = obter_algoritmos_disponiveis()
    print("Algoritmos disponíveis:")
    for numero, nome in enumerate(algoritmos, start=1):
        print(f"{numero}. {nome}")

    opcao = input("Escolha o algoritmo: ").strip()
    if not opcao.isdigit() or not 1 <= int(opcao) <= len(algoritmos):
        print("Opção de algoritmo inválida.")
        return

    algoritmo = algoritmos[int(opcao) - 1]
    origem = input("Ponto de origem: ")
    destino = input("Ponto de destino: ")

    try:
        resultado = executar_rota(grafo, origem, destino, algoritmo)
    except ValueError as erro:
        print(f"Não foi possível buscar a rota: {erro}")
        return

    if resultado is None:
        print("Não existe caminho entre esses pontos.")
        return

    caminho, custo = resultado
    print(f"Caminho encontrado: {' -> '.join(caminho)}")
    print(f"Custo total do caminho: {custo:g}")


def executar_menu():
    # Mantém o menu ativo até o usuário escolher sair.
    grafo = Grafo()

    while True:
        print("\n=== MetroNet ===")
        print("1. Cadastrar ponto")
        print("2. Cadastrar conexão")
        print("3. Consultar rede")
        print("4. Buscar caminho")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_ponto(grafo)
        elif opcao == "2":
            cadastrar_conexao(grafo)
        elif opcao == "3":
            exibir_rede(grafo)
        elif opcao == "4":
            buscar_rota(grafo)
        elif opcao == "0":
            print("Programa encerrado.")
            return
        else:
            print("Opção inválida. Escolha uma opção exibida no menu.")


if __name__ == "__main__":
    executar_menu()
