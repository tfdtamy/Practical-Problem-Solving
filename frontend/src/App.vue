<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import Viewer from './components/Viewer.vue'
import { getHealth } from './api'

// 后端状态：checking / ok / offline
const backend = ref('checking')
const version = ref('')
let timer = null

async function checkHealth() {
  try {
    const data = await getHealth()
    backend.value = data.status === 'ok' ? 'ok' : 'offline'
    version.value = data.version || ''
  } catch {
    backend.value = 'offline'
  }
}

onMounted(() => {
  checkHealth()
  timer = setInterval(checkHealth, 10000)
})

onUnmounted(() => clearInterval(timer))

const labels = { checking: '检测中…', ok: '后端在线', offline: '后端离线' }
</script>

<template>
  <header class="topbar">
    <span class="title">时叠 Chronoscope</span>
    <span class="subtitle">校园历史影像三维定位与定年</span>
  </header>

  <main class="stage">
    <Viewer src="/sample.ply" />
  </main>

  <div class="status" :class="backend">
    <span class="dot"></span>
    {{ labels[backend] }}<template v-if="backend === 'ok' && version"> · v{{ version }}</template>
  </div>
</template>

<style scoped>
.topbar {
  height: 48px;
  display: flex;
  align-items: baseline;
  gap: 12px;
  padding: 14px 16px 0;
  background: #26272b;
  border-bottom: 1px solid #333;
}

.title {
  font-weight: 600;
  font-size: 16px;
}

.subtitle {
  font-size: 13px;
  color: #9a9a9a;
}

.stage {
  height: calc(100% - 48px);
}

.status {
  position: fixed;
  right: 16px;
  bottom: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  background: rgba(0, 0, 0, 0.55);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #999;
}

.ok .dot {
  background: #3fb950;
}

.offline .dot {
  background: #f85149;
}
</style>
