const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
const AUTH_CHANGED_EVENT = "todo-auth-changed";
export function getAccessToken() {
    return localStorage.getItem("access_token");
}
export function setAccessToken(token) {
    localStorage.setItem("access_token", token);
    window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}
export function getRefreshToken() {
    return localStorage.getItem("refresh_token");
}
export function setRefreshToken(token) {
    localStorage.setItem("refresh_token", token);
    window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}
export function clearAuth() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    window.dispatchEvent(new Event(AUTH_CHANGED_EVENT));
}
export function onAuthChanged(handler) {
    window.addEventListener(AUTH_CHANGED_EVENT, handler);
    return () => window.removeEventListener(AUTH_CHANGED_EVENT, handler);
}
async function request(path, options = {}) {
    const token = getAccessToken();
    const headers = new Headers(options.headers);
    if (!headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }
    if (token) {
        headers.set("Authorization", `Bearer ${token}`);
    }
    let response;
    try {
        response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
    }
    catch {
        throw new Error("无法连接后端服务，请确认后端已启动。");
    }
    if (response.status === 401) {
        clearAuth();
    }
    if (!response.ok) {
        let message = `请求失败：${response.status}`;
        try {
            const payload = await response.json();
            message = payload.detail || message;
        }
        catch {
            // Keep the generic status message when the response body is not JSON.
        }
        throw new Error(message);
    }
    if (response.status === 204) {
        return null;
    }
    return response.json();
}
export const api = {
    login: (email, password) => request("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
    }),
    register: (email, password) => request("/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, password })
    }),
    listTasks: () => request("/tasks"),
    createTask: (title) => request("/tasks", {
        method: "POST",
        body: JSON.stringify({ title })
    }),
    deleteTask: (taskId) => request(`/tasks/${taskId}`, {
        method: "DELETE"
    }),
    updateTask: (taskId, payload) => request(`/tasks/${taskId}`, {
        method: "PATCH",
        body: JSON.stringify(payload)
    }),
    startPomodoro: (durationSec = 1500) => request("/pomodoro/start", {
        method: "POST",
        body: JSON.stringify({ duration_sec: durationSec, mode: "focus" })
    }),
    pausePomodoro: () => request("/pomodoro/pause", {
        method: "POST"
    }),
    resumePomodoro: () => request("/pomodoro/resume", {
        method: "POST"
    }),
    finishPomodoro: () => request("/pomodoro/finish", {
        method: "POST"
    }),
    currentPomodoro: () => request("/pomodoro/current"),
    dailyStats: () => request("/stats/daily"),
    weeklyStats: () => request("/stats/weekly")
};
