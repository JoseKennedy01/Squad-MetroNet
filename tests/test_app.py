from app import executar_menu


def test_menu_cadastra_rede_e_mostra_caminho(monkeypatch, capsys):
    entradas = iter([
        "1", "A",                 # Cadastra A
        "1", "B",                 # Cadastra B
        "1", "C",                 # Cadastra C
        "2", "A", "B", "2",       # Conecta A a B com peso 2
        "2", "B", "C", "3",       # Conecta B a C com peso 3
        "4", "1", "A", "C",       # Busca caminho com BFS
        "0",                      # Encerra
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Caminho encontrado: A -> B -> C" in saida
    assert "Custo da rota encontrada: 5" in saida
    assert "Programa encerrado." in saida


def test_menu_informa_quando_nao_existe_caminho(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "4", "1", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    assert "Não existe caminho entre esses pontos." in capsys.readouterr().out


def test_menu_avisa_quando_a_opcao_e_invalida(monkeypatch, capsys):
    entradas = iter(["9", "0"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Opção inválida." in saida
    assert "Programa encerrado." in saida


def test_menu_aceita_peso_decimal_com_virgula(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "2", "A", "B", "2,5",
        "4", "1", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Caminho encontrado: A -> B" in saida
    assert "Custo da rota encontrada: 2.5" in saida

def test_menu_executa_dfs_e_mostra_caminho_e_custo(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "1", "C",
        "2", "A", "B", "2",
        "2", "B", "C", "3",
        "4", "2", "A", "C",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Caminho encontrado: A -> B -> C" in saida
    assert "Custo da rota encontrada: 5" in saida


def test_menu_dijkstra_mostra_rota_de_menor_custo(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "1", "C",
        "2", "A", "B", "10",
        "2", "A", "C", "2",
        "2", "C", "B", "3",
        "4", "3", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Caminho encontrado: A -> C -> B" in saida
    assert "Custo da rota encontrada: 5" in saida


def test_menu_informa_peso_negativo_e_continua(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "2", "A", "B", "-1",
        "4", "1", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Não foi possível cadastrar a conexão:" in saida
    assert "peso não pode ser negativo" in saida
    assert "Não existe caminho entre esses pontos." in saida
    assert "Programa encerrado." in saida


def test_menu_avisa_quando_algoritmo_escolhido_e_invalido(monkeypatch, capsys):
    entradas = iter(["4", "9", "0"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Opção de algoritmo inválida." in saida
    assert "Programa encerrado." in saida


def test_menu_informa_ponto_inexistente_na_busca(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "4", "1", "A", "X",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Não foi possível buscar a rota:" in saida
    assert "não está cadastrado" in saida




def test_menu_trata_digito_unicode_invalido_no_algoritmo(monkeypatch, capsys):
    entradas = iter(["4", "²", "0"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Opção de algoritmo inválida." in saida
    assert "Programa encerrado." in saida


def test_menu_rejeita_identificador_vazio_e_continua(monkeypatch, capsys):
    entradas = iter(["1", "   ", "0"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Não foi possível cadastrar o ponto:" in saida
    assert "Programa encerrado." in saida


def test_menu_rejeita_peso_nao_numerico_sem_interromper(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "2", "A", "B", "abc",
        "4", "1", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Digite um peso numérico" in saida
    assert "Não existe caminho entre esses pontos." in saida
    assert "Programa encerrado." in saida


def test_menu_apresenta_objetivo_de_cada_algoritmo(monkeypatch, capsys):
    entradas = iter(["4", "0", "0"])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "1. BFS — caminho com menos conexões" in saida
    assert "2. DFS — exploração em profundidade" in saida
    assert "3. DIJKSTRA — caminho de menor custo acumulado" in saida

def test_menu_rejeita_origem_e_destino_vazios_e_continua(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "4", "1", "   ", "B",
        "4", "1", "A", "   ",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert saida.count("Não foi possível buscar a rota:") == 2
    assert "Programa encerrado." in saida

def test_menu_dijkstra_informa_quando_nao_existe_caminho(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "4", "3", "A", "B",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Não existe caminho entre esses pontos." in saida
    assert "Programa encerrado." in saida


def test_menu_dijkstra_informa_origem_e_destino_inexistentes(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "4", "3", "X", "A",
        "4", "3", "A", "X",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert saida.count("Não foi possível buscar a rota:") == 2
    assert "não está cadastrada" in saida
    assert "Programa encerrado." in saida

def test_menu_consulta_rede_vazia_e_rede_com_conexao(monkeypatch, capsys):
    entradas = iter([
        "3",
        "1", "A",
        "1", "B",
        "2", "A", "B", "5",
        "3",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "A rede ainda não possui pontos cadastrados." in saida
    assert "Pontos e conexões cadastrados:" in saida
    assert "- A: B (peso 5.0)" in saida
    assert "- B: A (peso 5.0)" in saida
    assert "Programa encerrado." in saida

def test_menu_informa_cadastros_repetidos_e_preserva_rede(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "A",
        "1", "B",
        "2", "A", "B", "3",
        "2", "A", "B", "8",
        "3",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert "Esse ponto já está cadastrado." in saida
    assert "A conexão informada já está cadastrada." in saida
    assert "- A: B (peso 3.0)" in saida
    assert "- B: A (peso 3.0)" in saida
    assert "peso 8.0" not in saida
    assert "Programa encerrado." in saida

def test_menu_rejeita_pesos_nao_finitos_e_preserva_rede(monkeypatch, capsys):
    entradas = iter([
        "1", "A",
        "1", "B",
        "2", "A", "B", "nan",
        "2", "A", "B", "inf",
        "2", "A", "B", "-inf",
        "3",
        "0",
    ])
    monkeypatch.setattr("builtins.input", lambda _mensagem: next(entradas))

    executar_menu()

    saida = capsys.readouterr().out
    assert saida.count("Não foi possível cadastrar a conexão:") == 3
    assert saida.count("O peso deve ser um número finito.") == 3
    assert "- A: sem conexões" in saida
    assert "- B: sem conexões" in saida
    assert "Programa encerrado." in saida