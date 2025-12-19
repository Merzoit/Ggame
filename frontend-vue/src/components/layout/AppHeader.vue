<template>
  <header class="app-header">
    <div class="header-content">
      <div class="user-section">
        <router-link to="/profile" class="avatar-wrapper">
          <img 
            :src="userAvatar" 
            alt="Avatar" 
            class="avatar"
          />
          <div class="level-badge">{{ userLevel }}</div>
        </router-link>
        <div class="user-info">
          <div class="username">{{ userName }}</div>
          <div class="user-stats">
            <span class="stat">
              <span class="stat-icon">🏆</span>
              <span>{{ userWins }}</span>
            </span>
          </div>
        </div>
      </div>
      
      <router-link to="/profile" class="settings-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="3"></circle>
          <path d="M12 1v6m0 6v6M5.64 5.64l4.24 4.24m4.24 4.24l4.24 4.24M1 12h6m6 0h6M5.64 18.36l4.24-4.24m4.24-4.24l4.24-4.24"></path>
        </svg>
      </router-link>
    </div>
    
    <!-- Валютная панель -->
    <div class="currency-bar">
      <div class="currency-item">
        <span class="currency-icon">🪙</span>
        <span class="currency-amount">{{ gameStore.userCoins }}</span>
      </div>
      <div class="currency-item">
        <span class="currency-icon">💰</span>
        <span class="currency-amount">{{ gameStore.userGold }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useGameStore } from '../../stores/game'

const gameStore = useGameStore()

const userName = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.username_telegram || 
         user?.first_name_telegram || 
         user?.username ||
         'Игрок'
})

const userAvatar = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.avatar || '/default-avatar.png'
})

const userLevel = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  const wins = user?.games_won || 0
  return Math.floor(wins / 10) + 1
})

const userWins = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.games_won || 0
})

function showSettings() {
  // TODO: Показать настройки
  console.log('Settings clicked')
}
</script>

<style scoped>
.app-header {
  background: var(--bg-secondary);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-wrapper {
  position: relative;
  width: 50px;
  height: 50px;
  display: block;
  text-decoration: none;
  cursor: pointer;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-lg);
  border: 2px solid var(--accent-primary);
  object-fit: cover;
  box-shadow: var(--shadow-glow);
}

.level-badge {
  position: absolute;
  bottom: -4px;
  right: -4px;
  background: linear-gradient(135deg, var(--accent-danger), var(--accent-warning));
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  border: 2px solid var(--bg-secondary);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.username {
  font-weight: 600;
  font-size: 16px;
  color: var(--text-primary);
}

.user-stats {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: var(--text-secondary);
}

.stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-icon {
  font-size: 14px;
}

.settings-btn {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 10px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.settings-btn:hover {
  background: var(--bg-card);
  color: var(--text-primary);
  border-color: var(--accent-primary);
}

.currency-bar {
  background: var(--bg-elevated);
  display: flex;
  justify-content: center;
  gap: 24px;
  padding: 10px 16px;
  border-top: 1px solid var(--border-color);
}

.currency-item {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-card);
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: 14px;
}

.currency-icon {
  font-size: 18px;
}

.currency-amount {
  color: var(--accent-primary);
}
</style>
