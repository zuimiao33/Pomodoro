<template>
  <div class="app-shell">
    <header class="app-topbar">
      <div class="brand-block">
        <p class="eyebrow">专注系统</p>
        <h1>任务清单 + 番茄钟</h1>
      </div>
      <nav class="nav-links">
        <RouterLink to="/tasks" class="nav-link">任务</RouterLink>
        <RouterLink to="/pomodoro" class="nav-link">番茄钟</RouterLink>
        <RouterLink to="/stats" class="nav-link">统计</RouterLink>
        <RouterLink to="/login" class="nav-link">账号</RouterLink>
        <button v-if="isAuthed" class="ghost-btn" @click="logout">退出</button>
      </nav>
    </header>
    <main class="app-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useRouter } from "vue-router";

import { clearAuth, getAccessToken, onAuthChanged } from "./api/client";

const router = useRouter();
const authVersion = ref(0);
const isAuthed = computed(() => {
  authVersion.value;
  return Boolean(getAccessToken());
});

let unsubscribe: (() => void) | null = null;

function logout() {
  clearAuth();
  router.push("/login");
}

onMounted(() => {
  unsubscribe = onAuthChanged(() => {
    authVersion.value += 1;
  });
});

onUnmounted(() => {
  if (unsubscribe) {
    unsubscribe();
    unsubscribe = null;
  }
});
</script>
