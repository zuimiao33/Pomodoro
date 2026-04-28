<template>
  <section class="surface">
    <div class="surface-head">
      <h2 class="surface-title">番茄钟</h2>
      <p class="muted">状态：{{ statusText }}</p>
    </div>
    <div class="timer-board">
      <p class="time-block">{{ display }}</p>
      <div class="meter">
        <div class="meter-fill" :style="{ width: `${progress}%` }"></div>
      </div>
      <div class="row">
        <button class="action-btn alt" @click="setPreset(25)">25 分钟</button>
        <button class="action-btn alt" @click="setPreset(15)">15 分钟</button>
        <button class="action-btn alt" @click="setPreset(5)">5 分钟</button>
      </div>
      <div class="row">
        <button class="action-btn" @click="start">开始</button>
        <button class="action-btn warn" @click="pause">暂停</button>
        <button class="action-btn alt" @click="resume">继续</button>
        <button class="action-btn danger" @click="finish">完成</button>
      </div>
    </div>
    <p class="tip" :class="{ error: isError }">{{ tip }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";

import { api } from "../api/client";

type PomodoroSession = {
  duration_sec: number;
  remaining_sec: number;
  status: "running" | "paused" | "completed" | "cancelled";
};

const remainingSec = ref(25 * 60);
const durationSec = ref(25 * 60);
const tip = ref("点击开始，进入专注。");
const isError = ref(false);
const status = ref<"idle" | PomodoroSession["status"]>("idle");

let timer: number | null = null;
let tickCount = 0;
let finishing = false;

const display = computed(() => {
  const minutes = Math.floor(remainingSec.value / 60);
  const seconds = remainingSec.value % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
});

const progress = computed(() => {
  if (durationSec.value <= 0) {
    return 0;
  }
  return Math.min(100, Math.max(0, ((durationSec.value - remainingSec.value) / durationSec.value) * 100));
});

const statusText = computed(() => {
  if (status.value === "idle") {
    return "未开始";
  }
  if (status.value === "running") {
    return "进行中";
  }
  if (status.value === "paused") {
    return "已暂停";
  }
  return "已完成";
});

function setPreset(minutes: number) {
  if (status.value === "running" || status.value === "paused") {
    tip.value = "当前已有进行中的番茄钟，请先完成后再切换时长。";
    isError.value = true;
    return;
  }
  durationSec.value = minutes * 60;
  remainingSec.value = durationSec.value;
  status.value = "idle";
  tip.value = `已选择 ${minutes} 分钟。`;
  isError.value = false;
}

function applySession(current: PomodoroSession | null) {
  if (!current) {
    if (status.value === "running" || status.value === "completed") {
      status.value = "completed";
      remainingSec.value = 0;
      return;
    }
    status.value = "idle";
    remainingSec.value = durationSec.value;
    return;
  }
  durationSec.value = current.duration_sec;
  remainingSec.value = current.remaining_sec;
  status.value = current.status;
}

async function syncCurrent() {
  try {
    const current = await api.currentPomodoro();
    applySession(current);
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "加载失败";
  }
}

async function start() {
  try {
    finishing = false;
    await api.startPomodoro(durationSec.value);
    await syncCurrent();
    tip.value = "番茄钟已开始。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "启动失败";
  }
}

async function pause() {
  try {
    await api.pausePomodoro();
    await syncCurrent();
    tip.value = "番茄钟已暂停。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "暂停失败";
  }
}

async function resume() {
  try {
    finishing = false;
    await api.resumePomodoro();
    await syncCurrent();
    tip.value = "番茄钟已继续。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "继续失败";
  }
}

async function finish() {
  try {
    await api.finishPomodoro();
    status.value = "completed";
    remainingSec.value = 0;
    tip.value = "本次番茄钟已完成。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "完成失败";
  }
}

async function finishWhenTimeIsUp() {
  if (finishing) {
    return;
  }
  finishing = true;
  try {
    await api.currentPomodoro();
    status.value = "completed";
    remainingSec.value = 0;
    tip.value = "时间到，本次番茄钟已完成。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "同步失败";
  }
}

onMounted(async () => {
  await syncCurrent();
  timer = window.setInterval(async () => {
    if (status.value === "running" && remainingSec.value > 0) {
      remainingSec.value -= 1;
      if (remainingSec.value === 0) {
        await finishWhenTimeIsUp();
      }
    }

    tickCount += 1;
    if (tickCount % 5 === 0 && remainingSec.value > 0) {
      await syncCurrent();
    }
  }, 1000);
});

onUnmounted(() => {
  if (timer) {
    window.clearInterval(timer);
    timer = null;
  }
});
</script>
