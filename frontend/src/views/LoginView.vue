<template>
  <section class="surface">
    <div class="surface-head">
      <h2 class="surface-title">账号</h2>
      <p class="muted">登录后同步任务和专注记录。</p>
    </div>
    <form @submit.prevent="handleSubmit" class="stack">
      <input v-model="email" class="field" placeholder="email@example.com" type="email" required />
      <input v-model="password" class="field" placeholder="密码（至少 6 位）" type="password" required />
      <div class="row">
        <button type="submit" class="action-btn">{{ mode === "login" ? "登录" : "注册" }}</button>
        <button type="button" class="action-btn alt" @click="toggleMode">
          {{ mode === "login" ? "切换到注册" : "切换到登录" }}
        </button>
      </div>
    </form>
    <p class="tip" :class="{ error: isError }">{{ tip }}</p>
    <p class="muted">首次使用请选择注册，注册成功后会自动登录。</p>
  </section>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

import { api, setAccessToken, setRefreshToken } from "../api/client";

type AuthMode = "login" | "register";

const router = useRouter();
const mode = ref<AuthMode>("login");
const email = ref("");
const password = ref("");
const tip = ref("欢迎回来。");
const isError = ref(false);

function toggleMode() {
  mode.value = mode.value === "login" ? "register" : "login";
  tip.value = mode.value === "login" ? "请输入账号和密码。" : "创建账号后即可开始使用。";
  isError.value = false;
}

async function handleSubmit() {
  try {
    const result =
      mode.value === "login"
        ? await api.login(email.value, password.value)
        : await api.register(email.value, password.value);
    setAccessToken(result.access_token);
    setRefreshToken(result.refresh_token);
    tip.value = "操作成功，正在跳转...";
    isError.value = false;
    router.push("/tasks");
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "认证失败";
  }
}
</script>
