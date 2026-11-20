# 09 — Preparação e demonstração ao vivo

## Preparação do ambiente (uma vez por computador)

1. Abra o Explorador de Arquivos e vá a `Documentos\Github\Squad-MetroNet`.
2. Abra um terminal nessa pasta (clique com o botão direito dentro da pasta e escolha **Abrir no Terminal**).
3. Confira se o Python está disponível:

```powershell
py --version
```

4. Crie um ambiente virtual e instale as dependências:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

O segundo comando usa diretamente o Python do ambiente virtual e não exige ativação. Aguarde o término sem mensagens de erro. Se `py` não for reconhecido, tente `python` nos comandos acima.

## Início rápido no dia da apresentação

1. Abra um terminal na raiz de `Squad-MetroNet`.
2. Inicie o único processo necessário:

```powershell
.\.venv\Scripts\python.exe app.py
```

3. Deixe esse terminal aberto. O sinal `Running on http://127.0.0.1:5000` indica que o servidor Flask está atendendo.
4. Abra o navegador em `http://127.0.0.1:5000`. Não abra `index.html` diretamente como arquivo: o navegador precisa receber a página e a API do mesmo servidor.
5. Confirme no topo da interface que o grafo foi carregado. Se quiser conferir a API, abra `http://127.0.0.1:5000/estacoes`; deve aparecer uma resposta JSON com nove estações.

Há apenas um terminal de servidor. As consultas e os cadastros são operados pelo navegador. A API e a interface são servidas pelo mesmo processo Flask; não é necessário iniciar `flask run` em outro terminal.

## Roteiro de consultas

A rede padrão tem nove estações e nove conexões; `EST03` fica isolada de propósito no caso de demonstração do PDF. Se necessário, use **Restaurar rede de demonstração** para voltar ao estado inicial. Para cada consulta, escolha origem `EST01`, destino `EST09` e o algoritmo no formulário, depois acione o botão de busca.

- **BFS:** caminho `EST01 → EST02 → EST09`, 2 conexões, custo 20. BFS minimiza a quantidade de conexões.
- **DFS:** caminho `EST01 → EST04 → EST07 → EST09`, 3 conexões, custo 14. A DFS apresenta o caminho encontrado conforme a ordem de exploração.
- **Dijkstra:** caminho `EST01 → EST04 → EST07 → EST09`, 3 conexões, custo 14. Dijkstra minimiza o custo acumulado.
- **Sem rota:** consulte `EST01` até `EST03`; a interface deve indicar que não foi encontrado caminho.

A tela apresenta o caminho, o custo, o número de conexões, as estações e a ordem de visita. A consulta `EST01`–`EST05` também tem rota (`EST01 → EST04 → EST05`, 2 conexões, custo 8); as demais estações conectadas não devem aparecer sem rota. BFS pode apresentar custo 20 embora exista uma rota de custo 14, porque escolhe a rota com menos conexões. Esse contraste é parte da explicação dos algoritmos.

## Encerrar e recuperar uma falha

- Para encerrar normalmente, volte ao terminal do Flask e pressione `Ctrl+C`.
- Se aparecer “Servidor Flask indisponível”, confirme que o terminal está aberto e mostra o endereço local; atualize a página do navegador.
- Se o terminal indicar que a porta 5000 já está ocupada, procure uma instância antiga do MetroNet. Encerre-a com `Ctrl+C` no terminal correspondente e inicie o servidor novamente.
- Se a página abrir mas mostrar resultado antigo após reiniciar, atualize-a. O grafo é mantido em memória e volta aos dados de demonstração quando o servidor reinicia.
- Antes de iniciar a apresentação, faça um ensaio completo com a mesma rede e o mesmo computador.

## Validação registrada

Em 20/11/2026, o comando `python app.py` foi iniciado e o endereço local respondeu pela rede HTTP. Página, CSS e JavaScript retornaram HTTP 200; a API listou nove estações e nove conexões; `EST03` fica isolada de propósito no caso de demonstração do PDF; BFS, DFS e Dijkstra retornaram os resultados acima; a consulta `EST01`–`EST03` retornou caminho nulo. A conferência visual e os erros no console do navegador ainda precisam ser verificados pela equipe.