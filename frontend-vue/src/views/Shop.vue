<template>
  <div class="shop-page">
    <div class="container">
      <div class="page-header">
        <h1>Магазин</h1>
      </div>

      <div class="shop-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Карты -->
      <div v-if="activeTab === 'cards'" class="shop-content">
        <div v-if="loading" class="loading">
          <div class="spinner"></div>
        </div>
        <div v-else class="shop-grid">
          <div
            v-for="template in gameStore.cardTemplates"
            :key="template.id"
            class="shop-item"
          >
            <div class="shop-item-image">🃏</div>
            <div class="shop-item-name">{{ template.name }}</div>
            <div class="shop-item-price">
              <span v-if="template.coin_cost > 0" class="price">
                <span class="currency-icon">🪙</span>
                {{ template.coin_cost }}
              </span>
              <span v-else class="price">
                <span class="currency-icon">💰</span>
                {{ template.gold_cost }}
              </span>
            </div>
            <button class="btn btn-primary shop-buy-btn" @click="buyCard(template)">
              Купить
            </button>
          </div>
        </div>
      </div>

      <!-- Предметы -->
      <div v-if="activeTab === 'items'" class="shop-content">
        <div class="empty-state">
          <div class="empty-icon">🛒</div>
          <div class="empty-text">Раздел в разработке</div>
        </div>
      </div>

      <!-- Валюта -->
      <div v-if="activeTab === 'currency'" class="shop-content">
        <div class="currency-packages">
          <div class="currency-package">
            <div class="package-icon">💰</div>
            <div class="package-info">
              <div class="package-name">Золотой пакет</div>
              <div class="package-price">99 ₽</div>
              <div class="package-reward">+500 золота</div>
            </div>
            <button class="btn btn-primary">Купить</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useGameStore } from '../stores/game'

const gameStore = useGameStore()
const activeTab = ref('cards')
const loading = ref(false)

const tabs = [
  { id: 'cards', label: 'Карты' },
  { id: 'items', label: 'Предметы' },
  { id: 'currency', label: 'Валюта' }
]

async function buyCard(template) {
  const success = await gameStore.acquireCard(template.id)
  if (success) {
    window.showToast?.(`Карта "${template.name}" куплена!`, 'success')
  } else {
    window.showToast?.('Не удалось купить карту. Проверьте баланс.', 'error')
  }
}

onMounted(async () => {
  loading.value = true
  await gameStore.fetchCardTemplates()
  loading.value = false
})
</script>

<style scoped>
.shop-page {
  padding: 20px 0;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shop-tabs {
  display: flex;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 4px;
  margin-bottom: 24px;
  gap: 4px;
}

.tab-btn {
  flex: 1;
  background: none;
  border: none;
  border-radius: var(--radius-sm);
  padding: 12px;
  color: var(--text-secondary);
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.tab-btn.active {
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  color: white;
  box-shadow: var(--shadow-sm);
}

.shop-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}

.shop-item {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.shop-item:hover {
  transform: translateY(-4px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-md);
}

.shop-item-image {
  width: 100%;
  height: 100px;
  background: var(--bg-elevated);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  margin-bottom: 12px;
}

.shop-item-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  margin-bottom: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.shop-item-price {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: var(--accent-primary);
  margin-bottom: 12px;
  font-size: 16px;
}

.currency-icon {
  font-size: 18px;
}

.shop-buy-btn {
  width: 100%;
  font-size: 13px;
  padding: 10px;
}

.currency-packages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.currency-package {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid var(--border-color);
}

.package-icon {
  font-size: 56px;
  opacity: 0.8;
}

.package-info {
  flex: 1;
}

.package-name {
  font-weight: 600;
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.package-price {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-primary);
  margin-bottom: 4px;
}

.package-reward {
  font-size: 14px;
  color: var(--text-secondary);
}
</style>
