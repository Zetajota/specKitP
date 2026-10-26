"use strict";

const state = { materias: [], tareas: [] };
const message = document.querySelector("#message");
const materiaForm = document.querySelector("#materia-form");
const tareaForm = document.querySelector("#tarea-form");
const filterMateria = document.querySelector("#filter-materia");
const filterEstado = document.querySelector("#filter-estado");
let classificationTimer;

function deliveryDeadline(fecha) {
  const [year, month, day] = fecha.split("-").map(Number);
  return new Date(year, month - 1, day + 1).getTime();
}

function temporalStatus(tarea, now = Date.now()) {
  if (tarea.completada) return "completada";
  const remaining = deliveryDeadline(tarea.fecha_entrega) - now;
  if (remaining <= 0) return "vencida";
  if (remaining <= 48 * 60 * 60 * 1000) return "urgente";
  return "normal";
}

function scheduleClassification() {
  clearTimeout(classificationTimer);
  const now = Date.now();
  const limits = state.tareas
    .filter(tarea => !tarea.completada)
    .flatMap(tarea => {
      const deadline = deliveryDeadline(tarea.fecha_entrega);
      return [deadline - 48 * 60 * 60 * 1000, deadline];
    })
    .filter(limit => limit > now);
  if (limits.length) {
    classificationTimer = setTimeout(
      renderTareas,
      Math.min(Math.min(...limits) - now, 2_147_483_647),
    );
  }
}

function showError(error) {
  message.textContent = error.message || "No se pudo completar la operación.";
  message.hidden = false;
}

function clearError() {
  message.textContent = "";
  message.hidden = true;
}

async function api(path, options) {
  let response;
  try {
    response = await fetch(path, options);
  } catch {
    throw new Error("No se pudo conectar con la aplicación.");
  }
  let data;
  try {
    data = await response.json();
  } catch {
    throw new Error("La aplicación devolvió una respuesta inválida.");
  }
  if (!response.ok) {
    throw new Error(data.error || "No se pudo completar la operación.");
  }
  return data;
}

function renderMaterias() {
  const list = document.querySelector("#materias-list");
  const select = document.querySelector("#tarea-materia");
  const selectedTaskMateria = select.value;
  const selectedFilterMateria = filterMateria.value;
  list.replaceChildren();
  select.replaceChildren();
  filterMateria.replaceChildren(new Option("Todas las materias", ""));
  document.querySelector("#empty-materias").hidden = state.materias.length > 0;
  for (const materia of state.materias) {
    const item = document.createElement("li");
    const mark = document.createElement("span");
    mark.className = "color-mark";
    mark.style.backgroundColor = materia.color;
    mark.setAttribute("aria-hidden", "true");
    item.append(mark, document.createTextNode(materia.nombre));
    list.append(item);
    const option = new Option(materia.nombre, String(materia.id));
    select.add(option);
    filterMateria.add(new Option(materia.nombre, String(materia.id)));
  }
  if (selectedTaskMateria) select.value = selectedTaskMateria;
  if (selectedFilterMateria) filterMateria.value = selectedFilterMateria;
  tareaForm.querySelector("button").disabled = state.materias.length === 0;
}

function renderTareas() {
  const list = document.querySelector("#tareas-list");
  list.replaceChildren();
  const empty = document.querySelector("#empty-tareas");
  empty.hidden = state.tareas.length > 0;
  empty.textContent = filterMateria.value || filterEstado.value
    ? "Ninguna tarea coincide con los filtros."
    : "Aún no hay tareas.";
  for (const tarea of state.tareas) {
    const item = document.createElement("li");
    const status = temporalStatus(tarea);
    item.classList.add(`task-${status}`);
    const title = document.createElement("strong");
    title.textContent = tarea.titulo;
    const materia = state.materias.find(value => value.id === tarea.materia_id);
    const details = document.createElement("p");
    details.textContent = `${materia?.nombre || "Materia"} · Entrega: ${tarea.fecha_entrega}`;
    item.append(title, details);
    if (status !== "normal") {
      const badge = document.createElement("span");
      badge.className = "status-badge";
      badge.textContent = {
        urgente: "Urgente",
        vencida: "Vencida",
        completada: "Completada",
      }[status];
      item.append(badge);
    }
    if (tarea.descripcion) {
      const description = document.createElement("p");
      description.textContent = tarea.descripcion;
      item.append(description);
    }
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = tarea.completada ? "Volver a pendiente" : "Completar";
    button.setAttribute(
      "aria-label",
      `${button.textContent} ${tarea.titulo}`,
    );
    button.addEventListener("click", async () => {
      clearError();
      try {
        await api(`/api/tareas/${tarea.id}/estado`, {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ completada: !tarea.completada }),
        });
        await refresh();
      } catch (error) {
        showError(error);
      }
    });
    item.append(button);
    list.append(item);
  }
  scheduleClassification();
}

async function refresh() {
  const query = new URLSearchParams();
  if (filterMateria.value) query.set("materia_id", filterMateria.value);
  if (filterEstado.value) query.set("estado", filterEstado.value);
  const [materias, tareas] = await Promise.all([
    api("/api/materias"),
    api(`/api/tareas${query.size ? `?${query}` : ""}`),
  ]);
  state.materias = materias;
  state.tareas = tareas;
  renderMaterias();
  renderTareas();
}

materiaForm.addEventListener("submit", async event => {
  event.preventDefault();
  clearError();
  const nombre = document.querySelector("#materia-nombre").value;
  const color = document.querySelector("#materia-color").value;
  try {
    await api("/api/materias", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, color }),
    });
    materiaForm.reset();
    await refresh();
  } catch (error) {
    showError(error);
  }
});

tareaForm.addEventListener("submit", async event => {
  event.preventDefault();
  clearError();
  const materia_id = Number(document.querySelector("#tarea-materia").value);
  const titulo = document.querySelector("#tarea-titulo").value;
  const descripcion = document.querySelector("#tarea-descripcion").value;
  const fecha_entrega = document.querySelector("#tarea-fecha").value;
  try {
    await api("/api/tareas", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ materia_id, titulo, descripcion, fecha_entrega }),
    });
    tareaForm.reset();
    await refresh();
  } catch (error) {
    showError(error);
  }
});

refresh().catch(showError);
filterMateria.addEventListener("change", () => refresh().catch(showError));
filterEstado.addEventListener("change", () => refresh().catch(showError));
document.querySelector("#clear-filters").addEventListener("click", () => {
  filterMateria.value = "";
  filterEstado.value = "";
  refresh().catch(showError);
});
window.addEventListener("focus", renderTareas);
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) renderTareas();
});
