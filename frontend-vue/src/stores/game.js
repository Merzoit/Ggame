import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../services/api'

export const useGameStore = defineStore('game', () => {
  // State
  const user = ref(null)
  const deck = ref(null)
  const inventory = ref([])
  const cardTemplates = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const userCoins = computed(() => user.value?.coins || 0)
  const userGold = computed(() => user.value?.gold || 0)
  const deckStats = computed(() => deck.value?.total_stats || { health: 0, attack: 0, defense: 0 })
  const isDeckValid = computed(() => deck.value?.is_valid_deck?.valid || false)

  // Actions
  async function fetchUser() {
    try {
      loading.value = true
      // TODO: Implement user API endpoint
      // user.value = await api.getUser()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  async function fetchDeck() {
    try {
      loading.value = true
      deck.value = await api.getDeck()
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch deck:', err)
    } finally {
      loading.value = false
    }
  }

  async function addCardToDeck(cardId, position) {
    try {
      loading.value = true
      await api.addCardToDeck(cardId, position)
      await fetchDeck()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  async function removeCardFromDeck(position) {
    try {
      loading.value = true
      await api.removeCardFromDeck(position)
      await fetchDeck()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  async function fetchInventory() {
    try {
      loading.value = true
      const data = await api.getInventory()
      inventory.value = Array.isArray(data) ? data : data.results || []
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch inventory:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchCardTemplates() {
    try {
      loading.value = true
      const data = await api.getCardTemplates()
      cardTemplates.value = Array.isArray(data) ? data : data.results || []
    } catch (err) {
      error.value = err.message
      console.error('Failed to fetch card templates:', err)
    } finally {
      loading.value = false
    }
  }

  async function acquireCard(templateId) {
    try {
      loading.value = true
      await api.acquireCard(templateId)
      await fetchDeck()
      await fetchUser()
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    user,
    deck,
    inventory,
    cardTemplates,
    loading,
    error,
    // Getters
    userCoins,
    userGold,
    deckStats,
    isDeckValid,
    // Actions
    fetchUser,
    fetchDeck,
    addCardToDeck,
    removeCardFromDeck,
    fetchInventory,
    fetchCardTemplates,
    acquireCard,
    clearError
  }
})
