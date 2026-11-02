# 07 — Execução do MetroNet

## 1. Requisitos

- Python 3 instalado.
- Acesso à pasta raiz do repositório.
- Dependências listadas em `requirements.txt` (`pytest` e `matplotlib`).

## 2. Preparar o ambiente no Windows PowerShell

Na pasta raiz do projeto, crie e ative um ambiente virtual e instale as dependências:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

O ambiente virtual mantém as dependências do projeto separadas das demais instalações do computador.

## 3. Iniciar a interface de terminal

Execute:

```powershell
python app.py
```

O menu permite cadastrar pontos, cadastrar conexões ponderadas, consultar a rede e buscar uma rota. Para encerrar, escolha `0`.

A rede começa vazia. Os cadastros feitos pelo menu permanecem em memória somente durante aquela execução. O menu usa uma rede não direcionada. Pesos decimais podem ser digitados com vírgula, como `2,5`.

## 4. Executar os testes

Na raiz do repositório, execute a suíte completa:

```powershell
python -m pytest -v
```

Para executar os testes de um módulo específico:

```powershell
python -m pytest -v tests/test_grafo.py
python -m pytest -v tests/test_busca_largura.py
python -m pytest -v tests/test_busca_profundidade.py
python -m pytest -v tests/test_dijkstra.py
python -m pytest -v tests/test_app.py
```

O modo `-v` mostra cada caso individualmente. Registre o comando, a versão do código e a saída observada para cada resultado compartilhado.

## 5. Módulos de dados e experimentos

O menu não possui opções para importar CSV ou gerar uma rede sintética. Essas funções estão separadas em `src/data/carregar_rede.py` e `src/data/gerar_rede_sintetica.py`.

Os scripts de benchmark e profiling ficam em `reports/profiling/` e são executados separadamente da interface. Eles podem atualizar CSVs, gráficos ou arquivos de perfil; coordene sua execução com a pessoa responsável por esses arquivos.

## 6. Roteiro curto de demonstração

Inicie o programa com `python app.py` e digite as opções abaixo, uma por vez. A rede usa conexões não direcionadas.

### Cadastrar os pontos

Escolha `1` e cadastre, nesta ordem: `A`, `B`, `C` e `D`.

### Cadastrar as conexões

Escolha `2` para cada conexão:

| Origem | Destino | Peso |
|---|---|---:|
| A | B | 10 |
| A | C | 2 |
| C | B | 3 |

O ponto `D` ficará sem conexões para demonstrar o caso sem rota.

### Comparar as buscas entre A e B

Escolha `4` para buscar uma rota, informe origem `A` e destino `B`, e selecione:

1. **BFS (opção 1):** mostra `A -> B`, custo `10`. Escolhe o caminho com menos conexões.
2. **DFS (opção 2):** nesta ordem de cadastro, mostra `A -> B`, custo `10`. A DFS retorna um caminho válido, mas não promete o menor custo.
3. **Dijkstra (opção 3):** mostra `A -> C -> B`, custo `5`, pois essa rota tem o menor custo acumulado.

### Demonstrar destino sem caminho

Escolha `4`, selecione BFS (`1`), informe origem `A` e destino `D`. O programa deve informar que não existe caminho entre esses pontos.

Para encerrar, escolha `0`. Os resultados acima foram conferidos no fluxo de terminal do aplicativo. A ordem de um caminho DFS pode depender da ordem dos vizinhos cadastrados.
