<template>
  <Teleport to="body">
    <div class="toast-container">
      <transition-group name="toast" tag="div">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['toast', `toast-${toast.type}`]"
        >
          <div class="toast-content">
            <span class="toast-message">{{ toast.message }}</span>
            <button class="toast-close" @click="removeToast(toast.id)">×</button>
          </div>
        </div>
      </transition-group>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const toasts = ref([])
let toastId = 0

function showToast(message, type = 'info', duration = 3000) {
  const id = toastId++
  toasts.value.push({ id, message, type })
  
  if (duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }
}

function removeToast(id) {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

onMounted(() => {
  // Экспортируем функцию для глобального использования
  window.showToast = showToast
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-lg);
  border-left: 4px solid;
  min-width: 300px;
  max-width: 400px;
  pointer-events: auto;
}

.toast-info {
  border-left-color: var(--accent-primary);
}

.toast-success {
  border-left-color: var(--accent-success);
}

.toast-warning {
  border-left-color: var(--accent-warning);
}

.toast-error {
  border-left-color: var(--accent-danger);
}

.toast-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.toast-message {
  color: var(--text-primary);
  font-size: 14px;
  flex: 1;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.toast-close:hover {
  color: var(--text-primary);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
