const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";
const AUTH_CHANGED_EVENT = "todo-auth-changed";

export function getAccessToken() {
  return localStorage.getItem("access_token");
}

export function setAccessToken(token: string) {
  localStorage.setItem("access_token", token);
  window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}

export function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

export function setRefreshToken(token: string) {
  localStorage.setItem("refresh_token", token);
  window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}

export function clearAuth() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}

export function onAuthChanged(handler: () => void) {
  window.addEventListener(AUTH_CHANGED_EVENT, handler);
  return () => window.removeEventListener(AUTH_CHANGED_EVENT, handler);
}

async function request(path: string, options: RequestInit = {}) {
  const token = getAccessToken();
  const headers = new Headers(options.headers);
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  if (response.status === 401) {
    clearAuth();
  }
  if (!response.ok) {
    try {
      const payload = await response.json();
      throw new Error(payload.detail || `请求失败：${response.status}`);
    } catch {
      const text = await response.text();
      throw new Error(text || `请求失败：${response.status}`);
    }
  }
  if (response.status === 204) {
    return null;
  }
  return response.json();
}

export const api = {
  login: (email: string, password: string) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    }),
  register: (email: string, password: string) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password })
    }),
  listTasks: () => request("/tasks"),
  createTask: (title: string) =>
    request("/tasks", {
      method: "POST",
      body: JSON.stringify({ title })
    }),
  deleteTask: (taskId: number) =>
    request(`/tasks/${taskId}`, {
      method: "DELETE"
    }),
  updateTask: (taskId: number, payload: Record<string, unknown>) =>
    request(`/tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify(payload)
    }),
  startPomodoro: (durationSec = 1500) =>
    request("/pomodoro/start", {
      method: "POST",
      body: JSON.stringify({ duration_sec: durationSec, mode: "focus" })
    }),
  pausePomodoro: () =>
    request("/pomodoro/pause", {
      method: "POST"
    }),
  resumePomodoro: () =>
    request("/pomodoro/resume", {
      method: "POST"
    }),
  finishPomodoro: () =>
    request("/pomodoro/finish", {
      method: "POST"
    }),
  currentPomodoro: () => request("/pomodoro/current"),
  dailyStats: () => request("/stats/daily"),
  weeklyStats: () => request("/stats/weekly")
};
