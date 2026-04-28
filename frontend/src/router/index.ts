import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import PomodoroView from "../views/PomodoroView.vue";
import StatsView from "../views/StatsView.vue";
import TasksView from "../views/TasksView.vue";
import { getAccessToken } from "../api/client";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/tasks" },
    { path: "/login", component: LoginView },
    { path: "/tasks", component: TasksView, meta: { requiresAuth: true } },
    { path: "/pomodoro", component: PomodoroView, meta: { requiresAuth: true } },
    { path: "/stats", component: StatsView, meta: { requiresAuth: true } }
  ]
});

router.beforeEach((to) => {
  const authed = Boolean(getAccessToken());
  if (to.meta.requiresAuth && !authed) {
    return "/login";
  }
  if (to.path === "/login" && authed) {
    return "/tasks";
  }
  return true;
});

export default router;
