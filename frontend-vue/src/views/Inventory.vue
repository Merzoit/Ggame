<template>
  <div class="inventory-page">
    <div class="container">
      <div class="page-header">
        <h1>Инвентарь</h1>
        <select v-model="filterType" class="filter-select">
          <option value="all">Все предметы</option>
          <option value="consumable">Расходуемые</option>
          <option value="equipment">Экипировка</option>
          <option value="collectible">Коллекционные</option>
        </select>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <div v-else-if="filteredInventory.length === 0" class="empty-state">
        <div class="empty-icon">🎒</div>
        <div class="empty-title">Инвентарь пуст</div>
        <div class="empty-text">Здесь появятся ваши предметы</div>
      </div>

      <div v-else class="inventory-grid">
        <div
          v-for="item in filteredInventory"
          :key="item.id"
          class="inventory-item"
          @click="showItemDetails(item)"
        >
          <div class="item-icon">{{ getItemIcon(item) }}</div>
          <div class="item-name">{{ item.name }}</div>
          <div v-if="item.quantity > 1" class="item-quantity">{{ item.quantity }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '../stores/game'

const gameStore = useGameStore()
const filterType = ref('all')
const loading = ref(false)

const filteredInventory = computed(() => {
  if (filterType.value === 'all') {
    return gameStore.inventory
  }
  return gameStore.inventory.filter(item => item.item_type === filterType.value)
})

function getItemIcon(item) {
  const icons = {
    consumable: '🧪',
    equipment: '⚔️',
    collectible: '🏆',
    currency: '💰'
  }
  return icons[item.item_type] || '📦'
}

function showItemDetails(item) {
  // TODO: Показать детали предмета
  window.showToast?.(`${item.name} - ${item.description || 'Нет описания'}`, 'info')
}

onMounted(async () => {
  loading.value = true
  await gameStore.fetchInventory()
  loading.value = false
})
</script>

<style scoped>
.inventory-page {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.filter-select {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
}

.inventory-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.inventory-item {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
}

.inventory-item:hover {
  transform: translateY(-4px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-md);
}

.item-icon {
  font-size: 40px;
  margin-bottom: 8px;
}

.item-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.item-quantity {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--accent-primary);
  color: white;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.empty-text {
  font-size: 14px;
}
</style>
