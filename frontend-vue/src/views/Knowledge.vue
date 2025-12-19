<template>
  <div class="knowledge-page">
    <div class="container">
      <div class="page-header">
        <h1>База знаний</h1>
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          placeholder="Поиск..."
        />
      </div>

      <div class="knowledge-content">
        <div class="categories-grid">
          <div
            v-for="category in filteredCategories"
            :key="category.id"
            class="category-card"
            :class="{ active: selectedCategory === category.id }"
            @click="selectCategory(category.id)"
          >
            <div class="category-icon">{{ category.icon }}</div>
            <div class="category-title">{{ category.title }}</div>
            <div class="category-description">{{ category.description }}</div>
          </div>
        </div>

        <div class="article-section">
          <div v-if="selectedCategory" class="article">
            <h2>{{ getCategoryTitle(selectedCategory) }}</h2>
            <div class="article-content" v-html="getCategoryContent(selectedCategory)"></div>
          </div>
          <div v-else class="article-placeholder">
            <div class="placeholder-icon">📖</div>
            <div class="placeholder-text">Выберите категорию для просмотра информации</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const selectedCategory = ref(null)

const categories = [
  {
    id: 'rules',
    icon: '📋',
    title: 'Правила игры',
    description: 'Основные правила и механики'
  },
  {
    id: 'cards',
    icon: '🃏',
    title: 'Карточки',
    description: 'Информация о картах и их свойствах'
  },
  {
    id: 'strategies',
    icon: '🎯',
    title: 'Стратегии',
    description: 'Советы по игре и тактикам'
  },
  {
    id: 'universe',
    icon: '🌟',
    title: 'Вселенные',
    description: 'Истории и лор аниме-вселенных'
  }
]

const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories
  const query = searchQuery.value.toLowerCase()
  return categories.filter(cat =>
    cat.title.toLowerCase().includes(query) ||
    cat.description.toLowerCase().includes(query)
  )
})

function selectCategory(categoryId) {
  selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
}

function getCategoryTitle(categoryId) {
  return categories.find(c => c.id === categoryId)?.title || ''
}

function getCategoryContent(categoryId) {
  const content = {
    rules: `
      <h3>Правила игры GGame</h3>
      <p>GGame - это коллекционная карточная игра в стиле аниме.</p>
      <ul>
        <li>Каждый игрок собирает колоду из 3 уникальных карт</li>
        <li>Карты имеют здоровье, атаку и защиту</li>
        <li>Разные стихии имеют преимущества друг над другом</li>
        <li>Побеждает игрок, у которого остались карты с здоровьем</li>
      </ul>
    `,
    cards: `
      <h3>Карточки</h3>
      <p>Карты - основной элемент игры. Каждая карта имеет:</p>
      <ul>
        <li><strong>Здоровье (HP)</strong> - сколько урона может выдержать карта</li>
        <li><strong>Атака (ATK)</strong> - урон, наносимый противнику</li>
        <li><strong>Защита (DEF)</strong> - снижение входящего урона</li>
        <li><strong>Стихия</strong> - элемент, влияющий на взаимодействие с другими картами</li>
      </ul>
    `,
    strategies: `
      <h3>Стратегии игры</h3>
      <p>Для победы важно:</p>
      <ul>
        <li>Подбирать сбалансированные колоды</li>
        <li>Учитывать преимущества стихий</li>
        <li>Правильно расставлять порядок карт в колоде</li>
        <li>Анализировать сильные и слабые стороны противника</li>
      </ul>
    `,
    universe: `
      <h3>Аниме-вселенные</h3>
      <p>GGame включает карты из различных аниме:</p>
      <ul>
        <li><strong>Naruto</strong> - Ниндзюцу и джутсу</li>
        <li><strong>One Piece</strong> - Пираты и способности</li>
        <li><strong>Dragon Ball</strong> - Сайянские техники</li>
        <li><strong>И многие другие</strong> - постоянно добавляются новые</li>
      </ul>
    `
  }
  return content[categoryId] || '<p>Информация по этой категории готовится...</p>'
}
</script>

<style scoped>
.knowledge-page {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  gap: 16px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.search-input {
  flex: 1;
  max-width: 300px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 10px 16px;
  color: var(--text-primary);
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-glow);
}

.knowledge-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 24px;
}

.categories-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  cursor: pointer;
  transition: var(--transition);
  border: 2px solid transparent;
}

.category-card:hover {
  transform: translateX(4px);
  border-color: var(--accent-primary);
}

.category-card.active {
  background: var(--bg-elevated);
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-md);
}

.category-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.category-title {
  font-weight: 600;
  font-size: 16px;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.category-description {
  font-size: 13px;
  color: var(--text-secondary);
}

.article-section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 24px;
  min-height: 400px;
}

.article h2 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--text-primary);
}

.article-content {
  color: var(--text-secondary);
  line-height: 1.8;
}

.article-content h3 {
  color: var(--text-primary);
  margin: 20px 0 12px;
  font-size: 18px;
}

.article-content ul {
  margin-left: 20px;
  margin-bottom: 16px;
}

.article-content li {
  margin-bottom: 8px;
}

.article-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-secondary);
  text-align: center;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.placeholder-text {
  font-size: 16px;
}

@media (max-width: 768px) {
  .knowledge-content {
    grid-template-columns: 1fr;
  }
}
</style>
