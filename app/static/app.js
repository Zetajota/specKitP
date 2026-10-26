"use strict";

const state = { materias: [], tareas: [] };
const message = document.querySelector("#message");
const materiaForm = document.querySelector("#materia-form");
const tareaForm = document.querySelector("#tarea-form");
const filterMateria = document.querySelector("#filter-materia");
const filterEstado = document.querySelector("#filter-estado");
let classificationTimer;
let reminderTimer;
let reminderCheck;
let reminderDay;
const displayedReminders = new Set();

function localDay(now = new Date()) {
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function nextLocalMidnight(now = new Date()) {
  return new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1).getTime();
}

function tomorrowLocalDay(now = new Date()) {
  return localDay(new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1));
}

function reminderList() {
  let section = document.querySelector("#recordatorios");
  if (!section) {
    section = document.createElement("section");
    section.id = "recordatorios";
    section.setAttribute("aria-labelledby", "recordatorios-title");
    section.setAttribute("aria-live", "polite");
    const heading = document.createElement("h2");
    heading.id = "recordatorios-title";
    heading.textContent = "Recordatorios";
    section.append(heading);
    document.querySelector("main").insertBefore(
      section,
      document.querySelector("#tareas-title").closest("section"),
    );
  }
  let list = section.querySelector("#recordatorios-list");
  if (!list) {
    list = document.createElement("ul");
    list.id = "recordatorios-list";
    section.append(list);
  }
  section.hidden = list.children.length === 0;
  return list;
}

function clearPreviousReminders(day) {
  if (reminderDay === day) return;
  reminderDay = day;
  displayedReminders.clear();
  reminderList().replaceChildren();
  document.querySelector("#recordatorios").hidden = true;
}

function showReminder(reminder) {
  const list = reminderList();
  const item = document.createElement("li");
  item.className = "recordatorio";
  const text = document.createElement("p");
  text.textContent =
    `${reminder.titulo} · ${reminder.materia} · Entrega: ${reminder.fecha_entrega}`;
  const close = document.createElement("button");
  close.type = "button";
  close.textContent = "Cerrar recordatorio";
  close.setAttribute("aria-label", `Cerrar recordatorio de ${reminder.titulo}`);
  close.addEventListener("click", () => {
    item.remove();
    document.querySelector("#recordatorios").hidden = list.children.length === 0;
  });
  item.append(text, close);
  list.append(item);
  document.querySelector("#recordatorios").hidden = false;
}

function scheduleReminders() {
  clearTimeout(reminderTimer);
  const now = new Date();
  reminderTimer = setTimeout(() => {
    checkReminders();
  }, Math.max(1, nextLocalMidnight(now) - now.getTime()));
}

async function checkReminders() {
  if (reminderCheck) return reminderCheck;
  reminderCheck = (async () => {
    const day = localDay();
    clearPreviousReminders(day);
    scheduleReminders();
    let candidates;
    try {
      candidates = await api(`/api/recordatorios?dia_local=${day}`);
    } catch (error) {
      // La aplicación base puede ejecutarse antes de incorporar la ruta nueva.
      if (!error.missingEndpoint) showError(error);
      return;
    }
    for (const reminder of candidates) {
      // Una respuesta tardía de ayer no debe crear avisos el día de entrega.
      if (localDay() !== day) return;
      if (reminder.fecha_entrega !== tomorrowLocalDay()) continue;
      if (displayedReminders.has(reminder.tarea_id)) continue;
      try {
        const result = await api(
          `/api/recordatorios/${reminder.tarea_id}/marcar`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ dia_local: day }),
          },
        );
        if (localDay() !== day) return;
        if (result.registrado === true) {
          displayedReminders.add(reminder.tarea_id);
          showReminder(reminder);
        }
      } catch (error) {
        showError(error);
      }
    }
  })();
  try {
    await reminderCheck;
  } finally {
    reminderCheck = null;
    // Si el día cambió durante la consulta, la evaluación de medianoche no se pierde.
    if (localDay() !== reminderDay) checkReminders();
  }
}

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
    const error = new Error(data.error || "No se pudo completar la operación.");
    error.status = response.status;
    error.missingEndpoint = response.status === 404 && !data.error;
    throw error;
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
  await checkReminders();
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
window.addEventListener("focus", () => {
  renderTareas();
  checkReminders();
});
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    renderTareas();
    checkReminders();
  }
});
