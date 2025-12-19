<template>
  <nav class="bottom-nav">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="nav-item"
      :class="{ active: $route.path === item.path }"
    >
      <div class="nav-icon">{{ item.icon }}</div>
      <div class="nav-label">{{ item.label }}</div>
    </router-link>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const navItems = ref([
  { path: '/', icon: '🃏', label: 'Колоды' },
  { path: '/inventory', icon: '🎒', label: 'Инвентарь' },
  { path: '/shop', icon: '🛒', label: 'Магазин' },
  { path: '/knowledge', icon: '📚', label: 'Знания' },
  { path: '/profile', icon: '👤', label: 'Профиль' }
])
</script>

<style scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-secondary);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-color);
  display: flex;
  padding: 6px 4px;
  z-index: 100;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.3);
  gap: 4px;
}

.nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 6px 4px;
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-secondary);
  transition: var(--transition);
  position: relative;
  min-width: 0;
}

.nav-item:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.nav-item.active {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  box-shadow: var(--shadow-sm);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  top: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 3px;
  background: var(--accent-primary);
  border-radius: 0 0 4px 4px;
}

.nav-icon {
  font-size: 22px;
  line-height: 1;
}

.nav-label {
  font-size: 10px;
  font-weight: 500;
  text-align: center;
}

@media (min-width: 768px) {
  .bottom-nav {
    display: none;
  }
}
</style>
