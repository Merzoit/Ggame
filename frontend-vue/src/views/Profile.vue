<template>
  <div class="profile-page">
    <div class="container">
      <!-- Заголовок профиля -->
      <div class="profile-header">
        <div class="profile-avatar-section">
          <div class="avatar-wrapper-large">
            <img 
              :src="userAvatar" 
              alt="Avatar" 
              class="avatar-large"
            />
            <div class="level-badge-large">{{ userLevel }}</div>
          </div>
          <div class="profile-info">
            <h1 class="username-large">{{ userName }}</h1>
            <div class="user-tag">{{ userTag }}</div>
          </div>
        </div>
      </div>

      <!-- Валюта -->
      <div class="currency-section">
        <div class="currency-card">
          <div class="currency-icon-large">🪙</div>
          <div class="currency-info">
            <div class="currency-label">Монеты</div>
            <div class="currency-value">{{ gameStore.userCoins }}</div>
          </div>
        </div>
        <div class="currency-card">
          <div class="currency-icon-large">💰</div>
          <div class="currency-info">
            <div class="currency-label">Золото</div>
            <div class="currency-value">{{ gameStore.userGold }}</div>
          </div>
        </div>
      </div>

      <!-- Статистика игрока -->
      <div class="stats-section">
        <h2 class="section-title">Статистика</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <div class="stat-value">{{ userStats.total_games || 0 }}</div>
              <div class="stat-label">Всего игр</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ userStats.games_won || 0 }}</div>
              <div class="stat-label">Побед</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <div class="stat-value">{{ winRate }}%</div>
              <div class="stat-label">Процент побед</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <div class="stat-value">{{ userStats.total_points || 0 }}</div>
              <div class="stat-label">Очки</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🔥</div>
            <div class="stat-content">
              <div class="stat-value">{{ userStats.current_streak || 0 }}</div>
              <div class="stat-label">Текущая серия</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">💎</div>
            <div class="stat-content">
              <div class="stat-value">{{ userStats.best_streak || 0 }}</div>
              <div class="stat-label">Лучшая серия</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Коллекция -->
      <div class="collection-section">
        <h2 class="section-title">Коллекция</h2>
        <div class="collection-stats">
          <div class="collection-stat">
            <div class="collection-value">{{ totalCards }}</div>
            <div class="collection-label">Всего карт</div>
          </div>
          <div class="collection-stat">
            <div class="collection-value">{{ uniqueCards }}</div>
            <div class="collection-label">Уникальных</div>
          </div>
          <div class="collection-stat">
            <div class="collection-value">{{ totalItems }}</div>
            <div class="collection-label">Предметов</div>
          </div>
        </div>
      </div>

      <!-- Информация о колоде -->
      <div class="deck-info-section">
        <h2 class="section-title">Моя колода</h2>
        <div v-if="gameStore.deck" class="deck-info">
          <div class="deck-stats-mini">
            <div class="mini-stat">
              <span class="mini-label">Здоровье:</span>
              <span class="mini-value">{{ gameStore.deckStats.health }}</span>
            </div>
            <div class="mini-stat">
              <span class="mini-label">Атака:</span>
              <span class="mini-value">{{ gameStore.deckStats.attack }}</span>
            </div>
            <div class="mini-stat">
              <span class="mini-label">Защита:</span>
              <span class="mini-value">{{ gameStore.deckStats.defense }}</span>
            </div>
          </div>
          <div class="deck-status">
            <span 
              class="status-badge"
              :class="{ valid: gameStore.isDeckValid, invalid: !gameStore.isDeckValid }"
            >
              {{ gameStore.isDeckValid ? '✓ Готова к бою' : '⚠ Не готова' }}
            </span>
          </div>
        </div>
        <router-link to="/" class="btn btn-primary">
          Редактировать колоду
        </router-link>
      </div>

      <!-- Настройки -->
      <div class="settings-section">
        <h2 class="section-title">Настройки</h2>
        <div class="settings-list">
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">Уведомления</div>
              <div class="setting-description">Получать уведомления о событиях</div>
            </div>
            <label class="toggle-switch">
              <input type="checkbox" v-model="settings.notifications" />
              <span class="toggle-slider"></span>
            </label>
          </div>
          <div class="setting-item">
            <div class="setting-info">
              <div class="setting-label">Язык</div>
              <div class="setting-description">Язык интерфейса</div>
            </div>
            <select v-model="settings.language" class="setting-select">
              <option value="ru">Русский</option>
              <option value="en">English</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Дополнительная информация -->
      <div class="info-section">
        <div class="info-item">
          <span class="info-label">Дата регистрации:</span>
          <span class="info-value">{{ formatDate(userStats.date_joined_telegram) }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Последняя активность:</span>
          <span class="info-value">{{ formatDate(userStats.last_activity) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useGameStore } from '../stores/game'
import api from '../services/api'

const route = useRoute()
const gameStore = useGameStore()
const settings = ref({
  notifications: true,
  language: 'ru'
})

const userStats = ref({
  total_games: 0,
  games_won: 0,
  total_points: 0,
  current_streak: 0,
  best_streak: 0,
  date_joined_telegram: null,
  last_activity: null
})

// Получаем user_id из URL параметров
const userId = computed(() => route.query.user_id)

const userName = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.username_telegram || 
         user?.first_name_telegram || 
         user?.username ||
         'Игрок'
})

const userTag = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.username_telegram ? 
         `@${user.username_telegram}` : 
         'Без тега'
})

const userAvatar = computed(() => {
  const user = gameStore.user || gameStore.deck?.owner
  return user?.avatar || '/default-avatar.png'
})

const userLevel = computed(() => {
  const wins = userStats.value.games_won || 0
  return Math.floor(wins / 10) + 1
})

const winRate = computed(() => {
  if (!userStats.value.total_games || userStats.value.total_games === 0) {
    return 0
  }
  return Math.round((userStats.value.games_won / userStats.value.total_games) * 100)
})

const totalCards = computed(() => {
  return userCards.value.length
})

const uniqueCards = computed(() => {
  const uniqueTemplates = new Set()
  userCards.value.forEach(card => {
    if (card.template) {
      uniqueTemplates.add(card.template.id)
    }
  })
  return uniqueTemplates.size
})

const userCards = ref([])

const totalItems = computed(() => {
  return gameStore.inventory.length
})

function formatDate(dateString) {
  if (!dateString) return 'Неизвестно'
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function loadUserStats() {
  try {
    // Если есть user_id в URL, загружаем данные конкретного пользователя
    if (userId.value) {
      console.log('Loading user data for telegram_id:', userId.value)
      const userData = await api.getUserByTelegramId(userId.value)

      if (userData) {
        userStats.value = {
          total_games: userData.total_games || 0,
          games_won: userData.games_won || 0,
          total_points: userData.total_points || 0,
          current_streak: userData.current_streak || 0,
          best_streak: userData.best_streak || 0,
          date_joined_telegram: userData.date_joined_telegram,
          last_activity: userData.last_activity
        }

        // Обновляем user в store
        gameStore.user = userData
        console.log('User data loaded:', userData)
      }
    } else {
      // Используем данные из deck или store (для обычной навигации)
      if (gameStore.deck?.owner) {
        const owner = gameStore.deck.owner
        userStats.value = {
          total_games: owner.total_games || 0,
          games_won: owner.games_won || 0,
          total_points: owner.total_points || 0,
          current_streak: owner.current_streak || 0,
          best_streak: owner.best_streak || 0,
          date_joined_telegram: owner.date_joined_telegram,
          last_activity: owner.last_activity
        }

        // Обновляем user в store
        if (!gameStore.user) {
          gameStore.user = owner
        }
      } else if (gameStore.user) {
        userStats.value = {
          total_games: gameStore.user.total_games || 0,
          games_won: gameStore.user.games_won || 0,
          total_points: gameStore.user.total_points || 0,
          current_streak: gameStore.user.current_streak || 0,
          best_streak: gameStore.user.best_streak || 0,
          date_joined_telegram: gameStore.user.date_joined_telegram,
          last_activity: gameStore.user.last_activity
        }
      }
    }
  } catch (error) {
    console.error('Failed to load user stats:', error)
  }
}

async function loadUserCards() {
  try {
    let cards
    if (userId.value) {
      // Загружаем карты конкретного пользователя
      cards = await api.getUserCardsByTelegramId(userId.value)
    } else {
      // Загружаем карты текущего пользователя
      cards = await api.getUserCards()
    }
    userCards.value = Array.isArray(cards) ? cards : cards.results || []
  } catch (error) {
    console.error('Failed to load user cards:', error)
  }
}

onMounted(async () => {
  await gameStore.fetchDeck()
  await gameStore.fetchInventory()
  await loadUserCards()
  await loadUserStats()
})
</script>

<style scoped>
.profile-page {
  padding: 20px 0;
  min-height: 100vh;
}

.profile-header {
  margin-bottom: 24px;
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  padding: 24px;
  border: 1px solid var(--border-color);
}

.avatar-wrapper-large {
  position: relative;
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.avatar-large {
  width: 100%;
  height: 100%;
  border-radius: var(--radius-xl);
  border: 3px solid var(--accent-primary);
  object-fit: cover;
  box-shadow: var(--shadow-glow);
}

.level-badge-large {
  position: absolute;
  bottom: -6px;
  right: -6px;
  background: linear-gradient(135deg, var(--accent-danger), var(--accent-warning));
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  border: 3px solid var(--bg-card);
  box-shadow: var(--shadow-md);
}

.profile-info {
  flex: 1;
}

.username-large {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-tag {
  font-size: 16px;
  color: var(--text-secondary);
  font-weight: 500;
}

.currency-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.currency-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.currency-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--accent-primary);
}

.currency-icon-large {
  font-size: 40px;
  opacity: 0.9;
}

.currency-info {
  flex: 1;
}

.currency-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.currency-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-primary);
}

.stats-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.stat-item {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.stat-item:hover {
  transform: translateY(-2px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  font-size: 32px;
  opacity: 0.8;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.collection-section {
  margin-bottom: 24px;
}

.collection-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.collection-stat {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-color);
}

.collection-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--accent-primary);
  margin-bottom: 8px;
}

.collection-label {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.deck-info-section {
  margin-bottom: 24px;
}

.deck-info {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 16px;
  border: 1px solid var(--border-color);
}

.deck-stats-mini {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.mini-stat {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mini-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.mini-value {
  font-size: 18px;
  font-weight: 600;
  color: var(--accent-primary);
}

.deck-status {
  margin-top: 12px;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 600;
}

.status-badge.valid {
  background: rgba(16, 185, 129, 0.2);
  color: var(--accent-success);
  border: 1px solid var(--accent-success);
}

.status-badge.invalid {
  background: rgba(239, 68, 68, 0.2);
  color: var(--accent-danger);
  border: 1px solid var(--accent-danger);
}

.settings-section {
  margin-bottom: 24px;
}

.settings-list {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  border: 1px solid var(--border-color);
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--border-color);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
}

.setting-label {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.setting-description {
  font-size: 13px;
  color: var(--text-secondary);
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 26px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--bg-elevated);
  transition: var(--transition);
  border-radius: 26px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: var(--transition);
  border-radius: 50%;
}

.toggle-switch input:checked + .toggle-slider {
  background-color: var(--accent-primary);
}

.toggle-switch input:checked + .toggle-slider:before {
  transform: translateX(24px);
}

.setting-select {
  background: var(--bg-elevated);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 8px 12px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
}

.info-section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  border: 1px solid var(--border-color);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.info-value {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

@media (max-width: 768px) {
  .profile-avatar-section {
    flex-direction: column;
    text-align: center;
  }

  .currency-section {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .collection-stats {
    grid-template-columns: 1fr;
  }
}
</style>
