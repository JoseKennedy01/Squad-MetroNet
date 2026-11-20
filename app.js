/* A interface consulta e altera o grafo mantido pela API Flask. */
(() => {
  "use strict";

  const API = "";
  const SVG_NS = "http://www.w3.org/2000/svg";
  const ALGORITHMS = ["bfs", "dfs", "dijkstra"];
  const NODE_STATES = ["is-origin", "is-dest", "is-visited", "is-path"];
  const DEFAULT_IDS = new Set(["EST01", "EST02", "EST03", "EST04", "EST05", "EST06", "EST07", "EST08", "EST09"]);
  const map = document.querySelector("#route-map");
  const routeForm = document.querySelector("#route-form");
  const stationForm = document.querySelector("#station-form");
  const connectionForm = document.querySelector("#connection-form");
  const stationLayer = map?.querySelector(".stations");
  const connectionLayer = map?.querySelector(".connections");
  const connectionList = document.querySelector("#connection-list");
  const customStationList = document.querySelector("#custom-station-list");
  const routeStatus = document.querySelector("#route-status");
  const connectionStatus = document.querySelector("#connection-status");
  const visitOrder = document.querySelector("#visit-order");
  const stationById = new Map();
  const customStations = [];
  let connections = [];
  let routeRun = 0;
  let lastRouteRequest = null;

  if (!map || !routeForm || !stationForm || !connectionForm || !stationLayer || !connectionLayer) return;

  function setStatus(element, message, kind = "") {
    if (!element) return;
    element.textContent = message;
    element.classList.toggle("is-error", kind === "error");
    element.classList.toggle("is-ok", kind === "ok");
  }

  async function requestJson(path, options = {}) {
    const headers = { Accept: "application/json", ...(options.headers || {}) };
    const requestOptions = { ...options, headers };
    if (options.body && typeof options.body !== "string") {
      headers["Content-Type"] = "application/json";
      requestOptions.body = JSON.stringify(options.body);
    }
    const response = await fetch(`${API}${path}`, requestOptions);
    const contentType = response.headers.get("content-type") || "";
    const body = contentType.includes("application/json") ? await response.json() : null;
    if (!response.ok) throw new Error(body?.erro || `Falha na API (${response.status}).`);
    return body;
  }

  function createSvgElement(name, attributes = {}) {
    const element = document.createElementNS(SVG_NS, name);
    Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, String(value)));
    return element;
  }

  function nextStationPosition() {
    const index = customStations.length;
    return { x: 100 + (index % 5) * 165, y: 550 + Math.floor(index / 5) * 120 };
  }

  function createStationNode(station, position) {
    const type = station.tipo === "carro" ? "carro" : "metro";
    const group = createSvgElement("g", {
      class: `station station--${type}`,
      "data-id": station.id,
      "data-x": position.x,
      "data-y": position.y,
      "data-nome": station.nome,
      "data-tipo": type,
      "data-custom": "true",
      transform: `translate(${position.x} ${position.y})`,
    });
    const title = createSvgElement("title");
    title.textContent = `${station.id} · ${station.nome} · ${type === "carro" ? "Carro" : "Metrô"}`;
    group.append(title);
    group.append(createSvgElement("circle", { class: "station__halo", r: 25 }));
    group.append(createSvgElement("circle", { class: "station__core", r: 16 }));
    const code = createSvgElement("text", { class: "station__code", y: 4 });
    code.textContent = station.id.match(/(\d+)$/)?.[1] || station.id.slice(-2);
    group.append(code);
    const name = createSvgElement("text", { class: "station__name", y: 45 });
    name.textContent = station.nome;
    group.append(name);
    const mode = createSvgElement("text", { class: "station__mode", y: 58 });
    mode.textContent = type === "carro" ? "Carro" : "Metrô";
    group.append(mode);
    stationLayer.append(group);
    return group;
  }

  function syncStations(records) {
    const recordsById = new Map(records.map((item) => [item.id, item]));
    map.querySelectorAll('.station[data-custom="true"]').forEach((node) => node.remove());
    stationById.clear();
    customStations.length = 0;

    map.querySelectorAll(".station[data-id]").forEach((node) => {
      const id = node.dataset.id;
      if (!recordsById.has(id)) node.remove();
    });

    records.forEach((record) => {
      const station = {
        id: record.id,
        nome: record.nome || record.id,
        tipo: record.tipo === "carro" ? "carro" : "metro",
        personalizada: Boolean(record.personalizada) || !DEFAULT_IDS.has(record.id),
      };
      let node = map.querySelector(`.station[data-id="${CSS.escape(station.id)}"]`);
      let position;
      if (node && !node.dataset.custom) {
        position = { x: Number(node.dataset.x), y: Number(node.dataset.y) };
        node.dataset.nome = station.nome;
        node.dataset.tipo = station.tipo;
        node.classList.remove("station--metro", "station--carro");
        node.classList.add(`station--${station.tipo}`);
        const name = node.querySelector(".station__name");
        if (name) name.textContent = station.nome;
        const mode = node.querySelector(".station__mode") || createSvgElement("text", { class: "station__mode", y: 58 });
        mode.textContent = station.tipo === "carro" ? "Carro" : "Metrô";
        if (!mode.parentNode) node.append(mode);
        const title = node.querySelector("title") || createSvgElement("title");
        title.textContent = `${station.id} · ${station.nome} · ${station.tipo === "carro" ? "Carro" : "Metrô"}`;
        if (!title.parentNode) node.prepend(title);
      } else {
        position = nextStationPosition();
        node = createStationNode(station, position);
      }
      station.x = position.x;
      station.y = position.y;
      station.node = node;
      stationById.set(station.id, station);
      if (station.personalizada) customStations.push(station);
    });

    updateMapViewport();
    refreshStationSelects();
    renderCustomStationList();
  }

  function updateMapViewport() {
    const height = Math.max(520, ...customStations.map((station) => station.y + 88));
    map.setAttribute("viewBox", `0 0 880 ${height}`);
    map.querySelector(".map-grid-bg")?.setAttribute("height", String(height));
    const stationCount = document.querySelector("#network-station-count");
    if (stationCount) stationCount.textContent = String(stationById.size).padStart(2, "0");
  }

  function refreshStationSelects() {
    const ids = [...stationById.keys()].sort((a, b) => a.localeCompare(b, "pt-BR", { numeric: true }));
    ["#origem", "#destino", "#connection-origin", "#connection-destination"].forEach((selector) => {
      const select = document.querySelector(selector);
      if (!select) return;
      const previous = select.value;
      select.replaceChildren();
      ids.forEach((id) => {
        const station = stationById.get(id);
        const option = document.createElement("option");
        option.value = id;
        option.textContent = `${id} · ${station.nome}`;
        select.append(option);
      });
      if (ids.includes(previous)) select.value = previous;
      else if (selector === "#destino") select.value = ids.includes("EST09") ? "EST09" : ids[ids.length - 1];
      else if (selector === "#connection-destination") select.value = ids.find((id) => id !== document.querySelector("#connection-origin")?.value) || ids[0];
      else select.value = ids.includes("EST01") ? "EST01" : ids[0];
    });
  }

  function makeConnection(edge) {
    const a = stationById.get(edge.origem);
    const b = stationById.get(edge.destino);
    if (!a || !b) return null;
    const group = createSvgElement("g", {
      class: "connection",
      "data-from": edge.origem,
      "data-to": edge.destino,
      "data-peso": edge.peso,
      "aria-label": `Conexão ${edge.origem} para ${edge.destino}, peso ${edge.peso}`,
    });
    group.append(createSvgElement("line", {
      class: "connection__line", x1: a.x, y1: a.y, x2: b.x, y2: b.y,
    }));
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const length = Math.hypot(dx, dy) || 1;
    const x = (a.x + b.x) / 2 - (dy / length) * 13;
    const y = (a.y + b.y) / 2 + (dx / length) * 13;
    const tag = createSvgElement("g", { class: "weight-tag", transform: `translate(${x} ${y})` });
    tag.append(createSvgElement("rect", { x: -17, y: -12, width: 34, height: 24, rx: 8 }));
    const text = createSvgElement("text", { y: 4 });
    text.textContent = String(edge.peso);
    tag.append(text);
    group.append(tag);
    return group;
  }

  function renderConnectionList() {
    connectionList.replaceChildren();
    connections.forEach((edge) => {
      const row = document.createElement("li");
      row.className = "connection-row";
      const details = document.createElement("span");
      details.className = "connection-row__details";
      details.textContent = `${edge.origem} ${stationById.get(edge.origem)?.nome || ""}`;
      const arrow = document.createElement("span");
      arrow.className = "connection-row__arrow";
      arrow.textContent = "↔";
      const destination = document.createElement("span");
      destination.textContent = `${edge.destino} ${stationById.get(edge.destino)?.nome || ""}`;
      const weight = document.createElement("span");
      weight.className = "connection-row__weight";
      weight.textContent = `${edge.peso} u.`;
      details.append(arrow, destination, weight);
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "connection-row__remove";
      remove.dataset.removeConnection = "true";
      remove.dataset.from = edge.origem;
      remove.dataset.to = edge.destino;
      remove.setAttribute("aria-label", `Remover conexão ${edge.origem} para ${edge.destino}`);
      remove.textContent = "Remover";
      row.append(details, remove);
      connectionList.append(row);
    });
  }

  function renderCustomStationList() {
    const list = document.querySelector("#custom-station-list");
    list.replaceChildren();
    const count = document.querySelector("#custom-station-total");
    if (count) count.textContent = `${customStations.length} ${customStations.length === 1 ? "estação" : "estações"}`;
    if (!customStations.length) {
      const empty = document.createElement("li");
      empty.className = "custom-station-empty";
      empty.textContent = "Nenhuma estação personalizada ainda.";
      list.append(empty);
      return;
    }
    customStations.forEach((station) => {
      const row = document.createElement("li");
      row.className = "custom-station-row";
      const name = document.createElement("span");
      name.className = "custom-station-row__name";
      name.textContent = `${station.id} · ${station.nome}`;
      const type = document.createElement("span");
      type.className = `custom-station-row__type${station.tipo === "carro" ? " custom-station-row__type--carro" : ""}`;
      type.textContent = station.tipo === "carro" ? "Carro" : "Metrô";
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "custom-station-remove";
      remove.dataset.removeStation = station.id;
      remove.setAttribute("aria-label", `Remover estação ${station.id} ${station.nome}`);
      remove.textContent = "×";
      row.append(name, type, remove);
      list.append(row);
    });
  }

  function clearRouteStates() {
    map.querySelectorAll(".station, .connection").forEach((element) => {
      ["is-origin", "is-dest", "is-visited", "is-path"].forEach((state) => element.classList.remove(state));
    });
  }

  function setCount(count, label = "nós") {
    const element = document.querySelector("#visit-count");
    if (!element) return;
    element.replaceChildren(document.createTextNode(String(count).padStart(2, "0")));
    const suffix = document.createElement("span");
    suffix.textContent = ` ${label}`;
    element.append(suffix);
  }

  function clearComparison(message) {
    document.querySelectorAll("[data-algo-row]").forEach((row) => {
      row.classList.remove("is-selected");
      row.querySelectorAll("[data-field]").forEach((cell) => { cell.textContent = "—"; });
    });
    const note = document.querySelector(".comparison-note");
    if (note) note.textContent = message;
  }

  function resetResults(message) {
    routeRun += 1;
    clearRouteStates();
    clearComparison("Aguardando nova busca");
    visitOrder.replaceChildren();
    setCount(0);
    ["#route-path", "#route-cost", "#route-stops"].forEach((selector) => {
      const element = document.querySelector(selector);
      if (element) element.textContent = "—";
    });
    const description = document.querySelector("#svg-description");
    if (description) description.textContent = message;
    setStatus(routeStatus, message);
  }

  function formatCost(value) {
    if (value === null || value === undefined) return "—";
    return `${new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 3 }).format(Number(value))} u.`;
  }

  function writeComparison(algo, result, selectedAlgo) {
    const row = document.querySelector(`[data-algo-row="${algo}"]`);
    if (!row) return;
    const path = Array.isArray(result.caminho) ? result.caminho : [];
    const visited = Array.isArray(result.visitados) ? result.visitados : [];
    row.classList.toggle("is-selected", algo === selectedAlgo);
    row.querySelector('[data-field="caminho"]').textContent = path.length ? path.join(" → ") : "Sem rota";
    row.querySelector('[data-field="paradas"]').textContent = path.length ? String(path.length) : "—";
    row.querySelector('[data-field="custo"]').textContent = formatCost(result.custo);
    row.querySelector('[data-field="visitados"]').textContent = String(visited.length);
  }

  function updateActiveAlgorithm(algo) {
    map.dataset.algo = algo;
    const badge = document.querySelector("#active-algorithm");
    if (!badge) return;
    badge.classList.remove("algo-badge--bfs", "algo-badge--dfs", "algo-badge--dijkstra");
    badge.classList.add(`algo-badge--${algo}`);
    badge.textContent = `${algo.toUpperCase()} ativo`;
  }

  function addVisitItem(id, index) {
    const item = document.createElement("li");
    item.className = "visit-order__item is-complete";
    item.dataset.visitId = id;
    const number = document.createElement("span");
    number.className = "visit-order__number";
    number.textContent = String(index + 1).padStart(2, "0");
    const code = document.createElement("span");
    code.className = "visit-order__code";
    code.textContent = id;
    const name = document.createElement("span");
    name.className = "visit-order__label";
    name.textContent = stationById.get(id)?.nome || "Estação";
    item.append(number, code, name);
    visitOrder.append(item);
  }

  function markPath(path) {
    path.forEach((id) => {
      map.querySelector(`.station[data-id="${CSS.escape(id)}"]`)?.classList.add("is-path");
      visitOrder.querySelector(`[data-visit-id="${CSS.escape(id)}"]`)?.classList.add("is-route-node");
    });
    path.slice(0, -1).forEach((from, index) => {
      const to = path[index + 1];
      map.querySelectorAll(".connection").forEach((edge) => {
        if ((edge.dataset.from === from && edge.dataset.to === to) ||
            (edge.dataset.from === to && edge.dataset.to === from)) edge.classList.add("is-path");
      });
    });
  }

  function updateRouteSummary(origin, destination, path, cost) {
    const ends = document.querySelectorAll("#route-summary .route-summary__endpoint span:last-child");
    if (ends[0]) ends[0].textContent = origin;
    if (ends[1]) ends[1].textContent = destination;
    document.querySelector("#route-path").textContent = path.length ? path.join(" → ") : "Sem rota encontrada";
    document.querySelector("#route-cost").textContent = formatCost(cost);
    document.querySelector("#route-stops").textContent = path.length ? `${path.length} estações` : "—";
    const description = document.querySelector("#svg-description");
    if (description) description.textContent = path.length
      ? `Rota de ${origin} a ${destination}: ${path.join(" para ")}. Custo ${formatCost(cost)}.`
      : `Não há rota entre ${origin} e ${destination} na rede atual.`;
  }

  function delay(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  async function getRoute(origin, destination, algo) {
    const query = new URLSearchParams({ origem: origin, destino: destination, algoritmo: algo });
    return requestJson(`/rota?${query}`);
  }

  async function traceRoute(origin, destination, algo) {
    const thisRun = ++routeRun;
    lastRouteRequest = { origin, destination, algo };
    clearRouteStates();
    updateActiveAlgorithm(algo);
    map.querySelector(`.station[data-id="${CSS.escape(origin)}"]`)?.classList.add("is-origin");
    map.querySelector(`.station[data-id="${CSS.escape(destination)}"]`)?.classList.add("is-dest");
    setStatus(routeStatus, `Consultando o grafo Python: ${origin} → ${destination} (${algo.toUpperCase()})…`);

    try {
      const pairs = await Promise.all(ALGORITHMS.map(async (name) => [name, await getRoute(origin, destination, name)]));
      if (thisRun !== routeRun) return;
      const results = Object.fromEntries(pairs);
      ALGORITHMS.forEach((name) => writeComparison(name, results[name], algo));
      const note = document.querySelector(".comparison-note");
      if (note) note.textContent = "Resultados calculados pelo Python";
      const caption = document.querySelector("#comparison-title + p");
      if (caption) caption.textContent = `Origem ${origin} · destino ${destination}. Paradas contam origem e destino.`;

      const result = results[algo];
      const path = Array.isArray(result.caminho) ? result.caminho : [];
      const visited = Array.isArray(result.visitados) ? result.visitados : [];
      updateRouteSummary(origin, destination, path, result.custo);
      visitOrder.replaceChildren();
      setCount(visited.length);
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      for (const [index, id] of visited.entries()) {
        if (thisRun !== routeRun) return;
        map.querySelector(`.station[data-id="${CSS.escape(id)}"]`)?.classList.add("is-visited");
        addVisitItem(id, index);
        if (!reducedMotion) await delay(90);
      }
      if (thisRun !== routeRun) return;

      if (path.length) {
        markPath(path);
        setStatus(routeStatus, `${algo.toUpperCase()} via Python · ${visited.length} nós visitados · custo ${formatCost(result.custo)}`, "ok");
      } else {
        setStatus(routeStatus, `Não há rota entre ${origin} e ${destination}.`, "error");
      }
    } catch (error) {
      if (thisRun !== routeRun) return;
      setStatus(routeStatus, `Falha ao consultar o Flask: ${error.message}`, "error");
    }
  }

  function readRouteForm() {
    const formData = new FormData(routeForm);
    return {
      origin: String(formData.get("origem")),
      destination: String(formData.get("destino")),
      algo: String(formData.get("algoritmo")).toLowerCase(),
    };
  }

  async function syncNetwork({ reroute = false, message = "Grafo sincronizado com o backend Python." } = {}) {
    const [stationData, connectionData] = await Promise.all([
      requestJson("/estacoes"),
      requestJson("/conexoes"),
    ]);
    syncStations(stationData.estacoes || []);
    connections = connectionData.conexoes || [];
    clearRouteStates();
    connectionLayer.replaceChildren();
    connections.forEach((edge) => {
      const group = makeConnection(edge);
      if (group) connectionLayer.append(group);
    });
    renderConnectionList();

    const total = document.querySelector("#connection-total");
    const edgeCount = document.querySelector("#network-edge-count");
    const footnoteCount = document.querySelector(".map-footnote__count");
    const title = document.querySelector("#svg-title");
    if (total) total.textContent = `${connections.length} ${connections.length === 1 ? "conexão" : "conexões"}`;
    if (edgeCount) edgeCount.textContent = String(connections.length).padStart(2, "0");
    if (footnoteCount) footnoteCount.textContent = `${connections.length} ${connections.length === 1 ? "aresta" : "arestas"}`;
    if (title) title.textContent = `Rede MetroNet com ${stationById.size} estações e ${connections.length} conexões`;
    resetResults(message);
    setStatus(connectionStatus, message, "ok");

    if (reroute && lastRouteRequest) {
      let { origin, destination, algo } = lastRouteRequest;
      if (!stationById.has(origin)) origin = document.querySelector("#origem").value;
      if (!stationById.has(destination)) destination = document.querySelector("#destino").value;
      lastRouteRequest = { origin, destination, algo };
      await traceRoute(origin, destination, algo);
    }
  }

  routeForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const { origin, destination, algo } = readRouteForm();
    traceRoute(origin, destination, algo);
  });

  stationForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(stationForm);
    try {
      const result = await requestJson("/estacoes", {
        method: "POST",
        body: { nome: String(data.get("nome")).trim(), tipo: String(data.get("tipo")) },
      });
      stationForm.reset();
      await syncNetwork({ reroute: true, message: `Estação ${result.estacao.id} adicionada ao grafo Python.` });
    } catch (error) {
      setStatus(connectionStatus, `Não foi possível adicionar a estação: ${error.message}`, "error");
    }
  });

  connectionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = new FormData(connectionForm);
    try {
      const result = await requestJson("/conexoes", {
        method: "POST",
        body: {
          origem: String(data.get("origem")),
          destino: String(data.get("destino")),
          peso: Number(data.get("peso")),
        },
      });
      await syncNetwork({ reroute: true, message: `Conexão ${result.origem} ↔ ${result.destino} adicionada ao grafo Python.` });
    } catch (error) {
      setStatus(connectionStatus, `Não foi possível adicionar a conexão: ${error.message}`, "error");
    }
  });

  connectionList.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-remove-connection]");
    if (!button) return;
    button.disabled = true;
    const query = new URLSearchParams({ origem: button.dataset.from, destino: button.dataset.to });
    try {
      await requestJson(`/conexoes?${query}`, { method: "DELETE" });
      await syncNetwork({ reroute: true, message: `Conexão ${button.dataset.from} ↔ ${button.dataset.to} removida do grafo Python.` });
    } catch (error) {
      button.disabled = false;
      setStatus(connectionStatus, `Não foi possível remover a conexão: ${error.message}`, "error");
    }
  });

  customStationList.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-remove-station]");
    if (!button) return;
    button.disabled = true;
    try {
      await requestJson(`/estacoes/${encodeURIComponent(button.dataset.removeStation)}`, { method: "DELETE" });
      await syncNetwork({ reroute: true, message: `Estação ${button.dataset.removeStation} e suas conexões foram removidas do grafo Python.` });
    } catch (error) {
      button.disabled = false;
      setStatus(connectionStatus, `Não foi possível remover a estação: ${error.message}`, "error");
    }
  });

  document.querySelector("#restore-demo")?.addEventListener("click", async () => {
    try {
      await requestJson("/rede/restaurar", { method: "POST" });
      document.querySelector("#origem").value = "EST01";
      document.querySelector("#destino").value = "EST09";
      document.querySelector("#algoritmo").value = "dijkstra";
      lastRouteRequest = { origin: "EST01", destination: "EST09", algo: "dijkstra" };
      await syncNetwork({ reroute: true, message: "Rede de demonstração restaurada no grafo Python." });
    } catch (error) {
      setStatus(connectionStatus, `Não foi possível restaurar o exemplo: ${error.message}`, "error");
    }
  });

  syncNetwork({ message: "Conectado ao grafo Python. Carregando a rota de demonstração…" })
    .then(() => {
      const { origin, destination, algo } = readRouteForm();
      return traceRoute(origin, destination, algo);
    })
    .catch((error) => {
      setStatus(connectionStatus, `Servidor Flask indisponível: ${error.message}. Inicie com python app.py.`, "error");
      setStatus(routeStatus, "Inicie o servidor Flask para consultar os algoritmos Python.", "error");
    });
})();
