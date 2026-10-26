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
    assert "Custo total do caminho: 5" in saida
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
    assert "Custo total do caminho: 2.5" in saida