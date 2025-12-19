<template>
  <div class="card-component" :class="{ editable }">
    <div class="card-header">
      <div class="card-name">{{ card.template_name || card.name }}</div>
      <div class="card-element" :style="{ background: elementColor }">
        {{ elementIcon }}
      </div>
    </div>
    
    <div class="card-stats">
      <div class="stat">
        <div class="stat-value">{{ card.health }}</div>
        <div class="stat-label">HP</div>
      </div>
      <div class="stat">
        <div class="stat-value">{{ card.attack }}</div>
        <div class="stat-label">ATK</div>
      </div>
      <div class="stat">
        <div class="stat-value">{{ card.defense }}</div>
        <div class="stat-label">DEF</div>
      </div>
    </div>
    
    <button v-if="editable" class="remove-btn" @click.stop="$emit('remove')">
      ✕
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  card: {
    type: Object,
    required: true
  },
  editable: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['remove'])

const elements = {
  fire: { icon: '🔥', color: 'rgba(239, 68, 68, 0.2)' },
  water: { icon: '💧', color: 'rgba(59, 130, 246, 0.2)' },
  earth: { icon: '🌱', color: 'rgba(34, 197, 94, 0.2)' },
  air: { icon: '💨', color: 'rgba(251, 191, 36, 0.2)' },
  light: { icon: '✨', color: 'rgba(251, 191, 36, 0.2)' },
  dark: { icon: '🌑', color: 'rgba(139, 92, 246, 0.2)' },
  neutral: { icon: '⚪', color: 'rgba(161, 161, 170, 0.2)' }
}

const element = computed(() => {
  const elementType = props.card.element || props.card.template?.element || 'neutral'
  return elements[elementType] || elements.neutral
})

const elementIcon = computed(() => element.value.icon)
const elementColor = computed(() => element.value.color)
</script>

<style scoped>
.card-component {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 16px;
  border: 2px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  cursor: pointer;
}

.card-component:hover {
  transform: translateY(-4px);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-lg), var(--shadow-glow);
}

.card-component.editable {
  cursor: default;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-name {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.card-element {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.card-stats {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}

.stat {
  flex: 1;
  text-align: center;
}

.stat-value {
  font-weight: 700;
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 10px;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.remove-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--accent-danger);
  color: white;
  border: none;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: var(--transition);
}

.card-component:hover .remove-btn {
  opacity: 1;
}

.remove-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}
</style>
