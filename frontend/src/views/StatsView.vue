<template>
  <section class="surface">
    <div class="surface-head">
      <h2 class="surface-title">专注统计</h2>
      <button class="action-btn alt" @click="load">刷新</button>
    </div>
    <div class="stats-grid">
      <article class="metric">
        <p>今日专注</p>
        <p>{{ formatDuration(day.focus_sec ?? 0) }}</p>
      </article>
      <article class="metric">
        <p>今日番茄数</p>
        <p>{{ day.session_count ?? 0 }}</p>
      </article>
      <article class="metric">
        <p>本周专注</p>
        <p>{{ formatDuration(week.focus_sec ?? 0) }}</p>
      </article>
      <article class="metric">
        <p>本周番茄数</p>
        <p>{{ week.session_count ?? 0 }}</p>
      </article>
    </div>
    <p class="tip" :class="{ error: isError }">{{ tip }}</p>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";

import { api } from "../api/client";

type StatsShape = {
  focus_sec?: number;
  session_count?: number;
};

const day = ref<StatsShape>({});
const week = ref<StatsShape>({});
const tip = ref("完成番茄钟后，统计会自动累计。");
const isError = ref(false);

function formatDuration(seconds: number) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours} 小时 ${minutes} 分钟`;
}

async function load() {
  try {
    day.value = await api.dailyStats();
    week.value = await api.weeklyStats();
    tip.value = "统计已刷新。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "加载失败";
  }
}

onMounted(load);
</script>
