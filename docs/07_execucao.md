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

Na etapa de busca, o menu também descreve o objetivo de cada opção: BFS procura um caminho com menos conexões, DFS explora a rede em profundidade e Dijkstra procura uma rota de menor custo acumulado.

Após a busca, o programa exibe o caminho encontrado e o campo "Custo da rota encontrada". Para BFS e DFS, o custo corresponde ao caminho retornado; somente Dijkstra busca minimizar esse custo.

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
python -m pytest -v tests/test_services.py
```

O modo `-v` mostra cada caso individualmente. Registre o comando, a versão do código e a saída observada para cada resultado compartilhado.

## 5. Módulos de dados e experimentos

O menu não possui opções para importar CSV ou gerar uma rede sintética. Essas funções estão separadas em `src/data/carregar_rede.py` e `src/data/gerar_rede_sintetica.py`.

Os scripts de benchmark e profiling ficam em `reports/profiling/` e são executados separadamente da interface. Eles podem atualizar CSVs, gráficos ou arquivos de perfil; coordene sua execução com a pessoa responsável por esses arquivos.

## 6. Roteiro curto de demonstração

Inicie o programa com `python app.py` e digite as opções abaixo, uma por vez. A rede usa conexões não direcionadas. A sequência reproduz o exemplo do PDF: Dijkstra encontra `EST01 -> EST04 -> EST07 -> EST09`, com custo total `14`.

### Cadastrar os pontos

Escolha `1` e cadastre, nesta ordem: `EST01`, `EST02`, `EST03`, `EST04`, `EST05`, `EST06`, `EST07`, `EST08` e `EST09`.

### Cadastrar as conexões

Escolha `2` para cada conexão:

| Origem | Destino | Peso |
|---|---|---:|
| EST01 | EST04 | 5 |
| EST04 | EST07 | 4 |
| EST07 | EST09 | 5 |
| EST01 | EST02 | 10 |
| EST02 | EST09 | 10 |

Os pontos `EST03`, `EST05`, `EST06` e `EST08` ficam sem conexões.

### Comparar as buscas entre EST01 e EST09

Escolha `4` para buscar uma rota, informe origem `EST01` e destino `EST09`, e selecione:

1. **BFS (opção 1):** mostra `EST01 -> EST02 -> EST09`, custo `20`, pois esse caminho tem menos conexões que o caminho pela sequência do exemplo do PDF.
2. **DFS (opção 2):** com esta ordem de cadastro, encontra `EST01 -> EST04 -> EST07 -> EST09`, custo `14`. A DFS retorna um caminho válido, mas não promete o menor custo.
3. **Dijkstra (opção 3):** mostra `EST01 -> EST04 -> EST07 -> EST09`, custo `14`, a rota de menor custo acumulado e a saída esperada no exemplo do PDF.

### Demonstrar destino sem caminho

Escolha `4`, selecione BFS (`1`), informe origem `EST01` e destino `EST03`. O programa deve informar que não existe caminho entre esses pontos.

Para encerrar, escolha `0`. Os resultados acima foram conferidos no fluxo de terminal do aplicativo. A ordem de um caminho DFS pode depender da ordem dos vizinhos cadastrados.
