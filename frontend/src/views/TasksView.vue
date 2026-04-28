<template>
  <section class="surface">
    <div class="surface-head">
      <h2 class="surface-title">任务面板</h2>
      <p class="muted">{{ summary }}</p>
    </div>
    <form class="row" @submit.prevent="handleCreate">
      <input v-model="newTitle" class="field" placeholder="写下你的下一步行动..." required />
      <button type="submit" class="action-btn">添加任务</button>
      <button type="button" class="action-btn alt" @click="loadTasks">刷新</button>
    </form>
    <ul class="list">
      <li v-for="task in tasks" :key="task.id">
        <div class="task-item">
          <div class="stack">
            <span class="task-title" :class="{ done: task.status === 'done' }">{{ task.title }}</span>
            <span class="pill" :class="task.status === 'done' ? 'done' : 'todo'">
              {{ task.status === "done" ? "已完成" : "待处理" }}
            </span>
          </div>
          <div class="row">
            <button class="action-btn warn" @click="markDone(task.id)" :disabled="task.status === 'done'">完成</button>
            <button class="action-btn danger" @click="removeTask(task.id)">删除</button>
          </div>
        </div>
      </li>
    </ul>
    <p class="tip" :class="{ error: isError }">{{ tip }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { api } from "../api/client";

type Task = {
  id: number;
  title: string;
  status: "todo" | "in_progress" | "done";
};

const tasks = ref<Task[]>([]);
const newTitle = ref("");
const tip = ref("");
const isError = ref(false);

const summary = computed(() => {
  const done = tasks.value.filter((task) => task.status === "done").length;
  return `共 ${tasks.value.length} 个任务，已完成 ${done} 个`;
});

async function loadTasks() {
  try {
    tasks.value = await api.listTasks();
    tip.value = tasks.value.length ? "保持节奏，一个一个清掉。" : "还没有任务，先添加第一个。";
    isError.value = false;
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "加载失败";
  }
}

async function handleCreate() {
  try {
    await api.createTask(newTitle.value);
    newTitle.value = "";
    await loadTasks();
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "创建失败";
  }
}

async function markDone(taskId: number) {
  try {
    await api.updateTask(taskId, { status: "done" });
    await loadTasks();
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "更新失败";
  }
}

async function removeTask(taskId: number) {
  try {
    await api.deleteTask(taskId);
    await loadTasks();
  } catch (error) {
    isError.value = true;
    tip.value = error instanceof Error ? error.message : "删除失败";
  }
}

onMounted(loadTasks);
</script>
