import csv
import math
from pathlib import Path
from src.models.grafo import Grafo

def carregar_rede(caminho_csv: str | Path) -> Grafo:
    # Converte o caminho recebido para um objeto Path.
    caminho = Path(caminho_csv)

    # Verifica se o caminho aponta para um arquivo existente.
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    grafo = Grafo(direcionado=False)

    try:
        with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)
            colunas_esperadas = ["origem", "destino", "peso"]

            # Rejeita arquivos sem cabeçalho.
            if leitor.fieldnames is None:
                raise ValueError("O CSV está vazio ou não possui cabeçalho.")

            # Remove espaços ao redor dos nomes das colunas.
            colunas_normalizadas = [
                coluna.strip() for coluna in leitor.fieldnames
            ]

            # Exige as três colunas na ordem definida pelo projeto.
            if colunas_normalizadas != colunas_esperadas:
                raise ValueError(
                    "O cabeçalho deve conter, nesta ordem: "
                    "origem, destino, peso."
                )

            # Atualiza as chaves utilizadas pelo DictReader.
            leitor.fieldnames = colunas_normalizadas

            # Processa cada conexão sem guardar todas as linhas em uma lista.
            quantidade_linhas = 0

            for numero_linha, linha in enumerate(leitor, start=2):
                quantidade_linhas += 1

                # Detecta valores excedentes em relação ao cabeçalho.
                if None in linha:
                    raise ValueError(
                        f"Linha {numero_linha}: existem colunas extras."
                    )

                # Normaliza os campos de texto.
                origem = (linha.get("origem") or "").strip()
                destino = (linha.get("destino") or "").strip()
                peso_texto = (linha.get("peso") or "").strip()

                # Impede o cadastro de conexões com campos vazios.
                if not origem or not destino or not peso_texto:
                    raise ValueError(
                        f"Linha {numero_linha}: "
                        "campos não podem ficar vazios."
                    )
                # Converte o peso para número.
                try:
                    peso = float(peso_texto)
                except ValueError as erro:
                    raise ValueError(
                        f"Linha {numero_linha}: peso deve ser numérico."
                    ) from erro

                # Rejeita NaN e valores infinitos.
                if not math.isfinite(peso):
                    raise ValueError(
                        f"Linha {numero_linha}: peso deve ser finito."
                    )

                # Rejeita conexões que ligam um ponto a ele mesmo.
                if origem == destino:
                    raise ValueError(
                        f"Linha {numero_linha}: "
                        "origem e destino são iguais."
                    )

                # Cadastra os pontos antes de criar a conexão.
                for ponto in (origem, destino):
                    grafo.adicionar_ponto(ponto)

                # Mantém a validação centralizada no modelo Grafo.
                try:
                    grafo.adicionar_conexao(origem, destino, peso)
                except ValueError as erro:
                    raise ValueError(
                        f"Linha {numero_linha}: "
                        f"conexão inválida: {erro}"
                    ) from erro

            # Mantém a regra atual: o CSV precisa ter conexões.
            if quantidade_linhas == 0:
                raise ValueError("O CSV não possui conexões.")

    except UnicodeDecodeError as erro:
        # Apresenta uma mensagem clara para arquivos com codificação inválida.
        raise ValueError(
            "O arquivo CSV não está codificado em UTF-8."
        ) from erro

    return grafo
