import csv
import math
from pathlib import Path
from src.models.grafo import Grafo

def carregar_rede(caminho_csv) -> Grafo:
    # Carrega conexões de um CSV e retorna um grafo válido.
    caminho = Path(caminho_csv)

    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    grafo = Grafo(direcionado=False)

    try:
        with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            colunas_esperadas = ["origem", "destino", "peso"]

            if leitor.fieldnames is None:
                raise ValueError("O CSV está vazio ou não possui cabeçalho.")

            colunas_originais = leitor.fieldnames
            colunas_normalizadas = [
                coluna.strip() for coluna in colunas_originais
            ]

            if colunas_normalizadas != colunas_esperadas:
                raise ValueError(
                    "O cabeçalho deve conter, nesta ordem: "
                    "origem, destino, peso."
                )

            # Padroniza as chaves usadas pelo DictReader.
            leitor.fieldnames = colunas_normalizadas
            linhas = list(leitor)

        if not linhas:
            raise ValueError("O CSV não possui conexões.")

        for numero_linha, linha in enumerate(linhas, start=2):
            if None in linha:
                raise ValueError(
                    f"Linha {numero_linha}: existem colunas extras."
                )

            origem = (linha.get("origem") or "").strip()
            destino = (linha.get("destino") or "").strip()
            peso_texto = (linha.get("peso") or "").strip()

            if not origem or not destino or not peso_texto:
                raise ValueError(
                    f"Linha {numero_linha}: campos não podem ficar vazios."
                )

            try:
                peso = float(peso_texto)
            except ValueError as erro:
                raise ValueError(
                    f"Linha {numero_linha}: peso deve ser numérico."
                ) from erro

            if not math.isfinite(peso):
                raise ValueError(
                    f"Linha {numero_linha}: peso deve ser finito."
                )

            if origem == destino:
                raise ValueError(
                    f"Linha {numero_linha}: origem e destino são iguais."
                )

            for ponto in (origem, destino):
                grafo.adicionar_ponto(ponto)

            try:
                grafo.adicionar_conexao(origem, destino, peso)
            except ValueError as erro:
                raise ValueError(
                    f"Linha {numero_linha}: conexão inválida: {erro}"
                ) from erro

    except UnicodeDecodeError as erro:
        raise ValueError(
            "O arquivo CSV não está codificado em UTF-8."
        ) from erro

    return grafo
