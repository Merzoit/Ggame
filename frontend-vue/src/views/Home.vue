<template>
  <div class="deck-page">
    <div class="container">
      <div class="page-header">
        <h1>Моя колода</h1>
        <button class="btn btn-primary" @click="editMode = !editMode">
          {{ editMode ? '💾 Сохранить' : '✏️ Редактировать' }}
        </button>
      </div>

      <!-- Статистика колоды -->
      <div class="deck-stats">
        <div class="stat-card">
          <div class="stat-value">{{ gameStore.deckStats.health }}</div>
          <div class="stat-label">Здоровье</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ gameStore.deckStats.attack }}</div>
          <div class="stat-label">Атака</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ gameStore.deckStats.defense }}</div>
          <div class="stat-label">Защита</div>
        </div>
      </div>

      <!-- Карты колоды -->
      <div class="deck-grid">
        <div
          v-for="(slot, index) in deckSlots"
          :key="index"
          class="deck-slot"
          :class="{ empty: !slot.card }"
          @click="editMode && handleSlotClick(index + 1)"
        >
          <CardComponent
            v-if="slot.card"
            :card="slot.card"
            :editable="editMode"
            @remove="removeCard(index + 1)"
          />
          <div v-else class="empty-slot">
            <div class="empty-icon">➕</div>
            <div class="empty-text">Добавить карту</div>
          </div>
        </div>
      </div>

      <!-- Валидация -->
      <div v-if="!gameStore.isDeckValid" class="deck-warning">
        <span class="warning-icon">⚠️</span>
        <span>{{ gameStore.deck?.is_valid_deck?.message || 'Колода не валидна' }}</span>
      </div>
    </div>

    <!-- Модальное окно выбора карты -->
    <CardSelectModal
      v-if="showCardModal"
      :position="selectedPosition"
      @close="showCardModal = false"
      @select="addCardToSlot"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGameStore } from '../stores/game'
import CardComponent from '../components/cards/CardComponent.vue'
import CardSelectModal from '../components/modals/CardSelectModal.vue'

const gameStore = useGameStore()
const editMode = ref(false)
const showCardModal = ref(false)
const selectedPosition = ref(1)

const deckSlots = computed(() => {
  const slots = [{ card: null }, { card: null }, { card: null }]
  
  if (gameStore.deck?.cards) {
    gameStore.deck.cards.forEach(deckCard => {
      const position = deckCard.position - 1
      if (position >= 0 && position < 3) {
        slots[position].card = deckCard.card_info || deckCard.card
      }
    })
  }
  
  return slots
})

function handleSlotClick(position) {
  selectedPosition.value = position
  showCardModal.value = true
}

async function addCardToSlot(cardId, position) {
  const success = await gameStore.addCardToDeck(cardId, position)
  if (success) {
    window.showToast?.('Карта добавлена в колоду', 'success')
    showCardModal.value = false
  } else {
    window.showToast?.('Не удалось добавить карту', 'error')
  }
}

async function removeCard(position) {
  const success = await gameStore.removeCardFromDeck(position)
  if (success) {
    window.showToast?.('Карта удалена из колоды', 'success')
  } else {
    window.showToast?.('Не удалось удалить карту', 'error')
  }
}

onMounted(async () => {
  await gameStore.fetchDeck()
})
</script>

<style scoped>
.deck-page {
  padding: 20px 0;
  min-height: 100vh;
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

.deck-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-md);
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--accent-primary);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.deck-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.deck-slot {
  min-height: 200px;
  border-radius: var(--radius-lg);
  transition: var(--transition);
}

.deck-slot.empty {
  cursor: pointer;
}

.empty-slot {
  background: var(--bg-elevated);
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-lg);
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 200px;
  transition: var(--transition);
}

.deck-slot.empty:hover .empty-slot {
  border-color: var(--accent-primary);
  background: var(--bg-card);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
}

.empty-text {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

.deck-warning {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--accent-danger);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--accent-danger);
  font-size: 14px;
}

.warning-icon {
  font-size: 20px;
}

@media (max-width: 768px) {
  .deck-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }
  
  .deck-stats {
    gap: 8px;
  }
  
  .stat-value {
    font-size: 24px;
  }
}
</style>
