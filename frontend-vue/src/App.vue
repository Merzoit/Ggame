<template>
  <div id="app">
    <!-- Шапка -->
    <AppHeader />
    
    <!-- Основной контент -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <!-- Нижняя навигация -->
    <AppNavigation />
    
    <!-- Toast уведомления -->
    <ToastContainer />
  </div>
</template>

<script setup>
import AppHeader from './components/layout/AppHeader.vue'
import AppNavigation from './components/layout/AppNavigation.vue'
import ToastContainer from './components/common/ToastContainer.vue'
</script>

<style scoped>
.main-content {
  flex: 1;
  padding-bottom: 80px; /* Для нижней навигации */
  min-height: calc(100vh - 140px);
}
</style>