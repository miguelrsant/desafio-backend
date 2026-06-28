const API = "";

function getToken() {
  return localStorage.getItem("token");
}

async function register() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  const response = await fetch(API + "/users/register", {
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
  } else {
    alert("Erro ao cadastrar");
  }
}

async function login() {
  const username = document.getElementById("username").value;

  const password = document.getElementById("password").value;

  const response = await fetch(API + "/users/login", {
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
    console.log(data);

    localStorage.setItem("token", data.data.access);

    window.location = "/dashboard";
  } else {
    alert("Login inválido");
  }
}

async function loadTasks() {
  const response = await fetch(API + "/tasks/", {
    headers: {
      Authorization: "Bearer " + getToken(),
    },
  });

  const result = await response.json();

  const tasks = result.data;

  const list = document.getElementById("tasks");

  list.innerHTML = "";

  tasks.forEach((task) => {
    list.innerHTML += `
        <li>
            <strong>${task.title}</strong>
            -
            ${task.description}
            -
            ${task.status}
        </li>
        `;
  });
}

async function createTask() {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  await fetch(API + "/tasks/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",

      Authorization: "Bearer " + getToken(),
    },

    body: JSON.stringify({
      title: title,

      description: description,
    }),
  });

  loadTasks();
}

function logout() {
  localStorage.removeItem("token");

  window.location = "/";
}
