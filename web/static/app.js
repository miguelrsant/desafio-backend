const API = "";

let taskEditando = null;

function getToken() {
  return localStorage.getItem("token");
}

async function register() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  const response = await fetch(API + "/api/users/register", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      username,
      password,
    }),
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.data.access);

    window.location = "/dashboard";
  }
}

async function login() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  const response = await fetch(API + "/api/users/login", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      username,
      password,
    }),
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.data.access);

    window.location = "/dashboard";
  }
}

async function loadTasks(url = "/api/tasks/") {
  const response = await fetch(API + url, {
    headers: {
      Authorization: "Bearer " + getToken(),
    },
  });

  const result = await response.json();

  const tasks = result.data;

  const list = document.getElementById("tasks");

  list.innerHTML = "";

  const Status = {
    COMPLETED: "Completo",
    PENDING: "Pendente",
    IN_PROGRESS: "Em progresso",
  };

  tasks.forEach((task) => {
    list.innerHTML += `
      <li>
        <div class="tarefas">
          <h1>${task.title}</h1>

          <p>${task.description}</p>

          <p>${Status[task.status]}</p>

          <div class="btns_tasks">
            <button onclick="alterarTask(${task.id})">Alterar</button>
            <button onclick="excluirTask(${task.id})">Excluir</button>
          </div>
        </div>
      </li>
        `;
  });
}

async function createTask() {
  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();

  if (!title || !description) {
    alert("Preencha o título e a descrição antes de criar a tarefa.");
    return;
  }

  await fetch(API + "/api/tasks/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + getToken(),
    },

    body: JSON.stringify({
      title,
      description,
      status: "PENDING",
    }),
  });

  document.getElementById("title").value = "";
  document.getElementById("description").value = "";

  loadTasks();
}

async function alterarTask(id) {
  taskEditando = id;

  const response = await fetch(API + `/api/tasks/${id}/`, {
    headers: {
      Authorization: "Bearer " + getToken(),
    },
  });

  const result = await response.json();

  console.log(result);

  const task = result.data ?? result;

  document.getElementById("editTitle").value = task.title;

  document.getElementById("editDescription").value = task.description;

  document.getElementById("editStatus").value = task.status;

  document.getElementById("editModal").style.display = "block";
}

async function saveEdit() {
  const title = document.getElementById("editTitle").value;

  const description = document.getElementById("editDescription").value;

  const status = document.getElementById("editStatus").value;

  await fetch(
    API + `/api/tasks/${taskEditando}/`,

    {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json",

        Authorization: "Bearer " + getToken(),
      },

      body: JSON.stringify({
        title: title,

        description: description,

        status: status,
      }),
    },
  );

  closeModal();

  loadTasks();
}

function closeModal() {
  document.getElementById("editModal").style.display = "none";
}

async function excluirTask(id) {
  await fetch(
    API + `/api/tasks/${id}/`,

    {
      method: "DELETE",

      headers: {
        Authorization: "Bearer " + getToken(),
      },
    },
  );

  loadTasks();
}

function logout() {
  localStorage.removeItem("token");

  window.location = "/";
}
function filterTasks() {
  const title = document.getElementById("filterTitle").value;

  const status = document.getElementById("filterStatus").value;

  let url = "/api/tasks/?";

  if (title) {
    url += `title=${title}&`;
  }

  if (status) {
    url += `status=${status}`;
  }

  loadTasks(url);
}

function clearFilters() {
  document.getElementById("filterTitle").value = "";

  document.getElementById("filterStatus").value = "";

  loadTasks();
}
