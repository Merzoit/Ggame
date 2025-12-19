<template>
  <Teleport to="body">
    <div class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Выберите карту для позиции {{ position }}</h3>
          <button class="modal-close" @click="$emit('close')">×</button>
        </div>
        
        <div class="modal-body">
          <div v-if="loading" class="loading">
            <div class="spinner"></div>
          </div>
          
          <div v-else-if="availableCards.length === 0" class="empty-state">
            <div class="empty-icon">🃏</div>
            <div class="empty-text">Нет доступных карт</div>
          </div>
          
          <div v-else class="cards-grid">
            <div
              v-for="card in availableCards"
              :key="card.id"
              class="selectable-card"
              @click="selectCard(card.id)"
            >
              <CardComponent :card="formatCardData(card)" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api'
import CardComponent from '../cards/CardComponent.vue'

const props = defineProps({
  position: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close', 'select'])

const loading = ref(true)
const availableCards = ref([])

async function loadAvailableCards() {
  try {
    loading.value = true
    const cards = await api.getUserCards()
    // Фильтруем карты, которые не в колоде
    availableCards.value = cards.filter(card => !card.is_in_deck)
  } catch (error) {
    console.error('Failed to load cards:', error)
    window.showToast?.('Не удалось загрузить карты', 'error')
  } finally {
    loading.value = false
  }
}

function formatCardData(card) {
  // Форматируем данные карты для CardComponent
  if (card.card_info) {
    return card.card_info
  }
  if (card.template) {
    return {
      template_name: card.template.name,
      element: card.template.element,
      health: card.health,
      attack: card.attack,
      defense: card.defense
    }
  }
  return card
}

function selectCard(cardId) {
  emit('select', cardId, props.position)
}

onMounted(() => {
  loadAvailableCards()
})
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: var(--bg-secondary);
  border-radius: var(--radius-xl);
  padding: 24px;
  max-width: 600px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: var(--transition);
}

.modal-close:hover {
  background: var(--bg-elevated);
  color: var(--text-primary);
}

.modal-body {
  min-height: 200px;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 12px;
}

.selectable-card {
  cursor: pointer;
  transition: var(--transition);
}

.selectable-card:hover {
  transform: scale(1.05);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
