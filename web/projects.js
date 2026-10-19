(() => {
  "use strict";

  const element = (id) => document.getElementById(id);

  const assistantView = element("assistant-view");
  const projectsView = element("projects-view");

  const assistantButton = element("assistant-view-button");
  const projectsButton = element("projects-view-button");
  const resetButton = element("reset-button");

  const catalog = element("project-catalog");
  const detail = element("project-detail");
  const feedback = element("projects-feedback");
  const retryButton = element("projects-retry");

  const statusLabels = {
    planned: "Запланировано",
    active: "В работе",
    done: "Готово",
  };

  let loaded = false;
  let loading = false;
  let selectedCard = null;

  function switchView(view) {
    const showProjects = view === "projects";

    assistantView.hidden = showProjects;
    projectsView.hidden = !showProjects;

    assistantButton.setAttribute(
      "aria-pressed",
      String(!showProjects),
    );

    projectsButton.setAttribute(
      "aria-pressed",
      String(showProjects),
    );

    if (resetButton) {
      resetButton.hidden = showProjects;
    }

    if (showProjects && !loaded) {
      loadProjects();
    }
  }

  function validateProjects(data) {
    if (!data || !Array.isArray(data.projects)) {
      throw new Error("Catalog must contain a projects array");
    }

    const requiredFields = [
      "id",
      "name",
      "icon",
      "description",
      "stage",
      "device_status",
      "goal",
    ];

    const ids = new Set();

    for (const project of data.projects) {
      if (
        !project ||
        requiredFields.some(
          (field) =>
            typeof project[field] !== "string" ||
            !project[field].trim(),
        )
      ) {
        throw new Error("Invalid project fields");
      }

      if (ids.has(project.id)) {
        throw new Error("Duplicate project ID");
      }

      ids.add(project.id);

      if (
        project.last_update !== null &&
        typeof project.last_update !== "string"
      ) {
        throw new Error("Invalid project update");
      }

      if (
        !Array.isArray(project.tasks) ||
        project.tasks.some(
          (task) =>
            !task ||
            typeof task.title !== "string" ||
            !task.title.trim() ||
            !Object.hasOwn(statusLabels, task.status),
        )
      ) {
        throw new Error("Invalid project tasks");
      }
    }

    return data.projects;
  }

  function createCard(project) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "project-card";

    const icon = document.createElement("span");
    icon.className = "project-card-icon";
    icon.textContent = project.icon;
    icon.setAttribute("aria-hidden", "true");

    const name = document.createElement("strong");
    name.textContent = project.name;

    const stage = document.createElement("span");
    stage.textContent = project.stage;

    const action = document.createElement("span");
    action.className = "project-card-action";
    action.textContent = "Открыть проект →";

    button.append(icon, name, stage, action);

    button.addEventListener("click", () => {
      openProject(project, button);
    });

    return button;
  }

  function renderTasks(tasks) {
    const list = element("project-task-list");
    list.replaceChildren();

    for (const task of tasks) {
      const item = document.createElement("li");

      const title = document.createElement("span");
      title.textContent = task.title;

      const status = document.createElement("span");
      status.className = "task-status";
      status.dataset.status = task.status;
      status.textContent = statusLabels[task.status];

      item.append(title, status);
      list.append(item);
    }

    const completed = tasks.filter(
      (task) => task.status === "done",
    ).length;

    element("project-task-count").textContent =
      `${completed} / ${tasks.length} выполнено`;
  }

  function openProject(project, card) {
    selectedCard = card;

    element("project-icon").textContent = project.icon;
    element("project-name").textContent = project.name;
    element("project-description").textContent = project.description;
    element("project-stage").textContent = project.stage;
    element("project-device").textContent = project.device_status;
    element("project-goal").textContent = project.goal;

    element("project-update").textContent =
      project.last_update || "Запись о прогрессе пока не добавлена";

    renderTasks(project.tasks);

    catalog.hidden = true;
    feedback.hidden = true;
    detail.hidden = false;

    element("project-name").focus();
  }

  function closeProject() {
    detail.hidden = true;
    catalog.hidden = false;
    feedback.hidden = false;

    selectedCard?.focus();
  }

  async function loadProjects() {
    if (loading) return;

    loading = true;
    retryButton.hidden = true;
    feedback.textContent = "Загрузка каталога…";

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    try {
      const response = await fetch("/static/projects.json", {
        signal: controller.signal,
        cache: "no-store",
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      const projects = validateProjects(await response.json());

      catalog.replaceChildren();

      for (const project of projects) {
        catalog.append(createCard(project));
      }

      feedback.textContent = projects.length
        ? `Проектов: ${projects.length}. Выберите карточку.`
        : "Проектов пока нет. Добавьте первый в projects.json.";

      loaded = true;
    } catch (error) {
      console.error("Project catalog loading failed:", error);

      feedback.textContent =
        "Не удалось загрузить каталог. Проверьте projects.json " +
        "и повторите попытку.";

      retryButton.hidden = false;
    } finally {
      clearTimeout(timeoutId);
      loading = false;
    }
  }

  assistantButton.addEventListener("click", () => {
    switchView("assistant");
  });

  projectsButton.addEventListener("click", () => {
    switchView("projects");
  });

  element("project-back").addEventListener("click", closeProject);
  retryButton.addEventListener("click", loadProjects);
})();