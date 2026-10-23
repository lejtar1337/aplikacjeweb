const API_URL = "http://127.0.0.1:8000";

export async function fetchTasks() {
  const response = await fetch(`${API_URL}/tasks`);
  const data = await response.json();
  return data.items;
}

export async function createTask(task) {
  const response = await fetch(`${API_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(task),
  });
  return response.json();
}