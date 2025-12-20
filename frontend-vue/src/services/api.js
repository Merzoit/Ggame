import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://web-production-051b.up.railway.app/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor для добавления токена
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url)
    const token = localStorage.getItem('ggame_token')
    console.log('🔑 Token:', token ? 'present' : 'missing')
    if (token) {
      config.headers.Authorization = `Token ${token}`
      console.log('✅ Auth header added')
    }
    return config
  },
  (error) => {
    console.error('❌ Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => {
    console.log('📨 API Response:', response.status, response.config.url)
    return response.data
  },
  (error) => {
    console.error('❌ API Error:', error.response?.status, error.response?.data || error.message)
    const message = error.response?.data?.message || error.response?.data?.error || error.message
    return Promise.reject(new Error(message))
  }
)

export default {
  // Deck endpoints
  getDeck() {
    return api.get('/cards/decks/')
  },

  updateDeck(data) {
    return api.put('/cards/decks/', data)
  },

  addCardToDeck(cardId, position) {
    return api.post('/cards/decks/add_card/', {
      card_id: cardId,
      position
    })
  },

  removeCardFromDeck(cardId) {
    return api.post('/cards/decks/remove_card/', {
      card_id: cardId
    })
  },

  // Cards endpoints
  getCardTemplates(params = {}) {
    return api.get('/cards/card-templates/', { params })
  },

  getUserCards() {
    return api.get('/cards/card-instances/')
  },

  acquireCard(templateId) {
    return api.post('/cards/card-instances/acquire_card/', {
      template_id: templateId
    })
  },

  sellCard(cardId) {
    return api.post(`/cards/card-instances/${cardId}/sell_card/`)
  },

  // Inventory endpoints
  getInventory() {
    return api.get('/inventory/inventory/')
  },

  getItems(params = {}) {
    return api.get('/inventory/items/', { params })
  },

  // Anime universes and seasons
  getAnimeUniverses() {
    return api.get('/cards/anime-universes/')
  },

  getSeasons(universeId = null) {
    const params = universeId ? { universe: universeId } : {}
    return api.get('/cards/seasons/', { params })
  },

  // User endpoints
  getCurrentUser() {
    return api.get('/users/me/')
  },

  getUserProfile() {
    return api.get('/cards/card-instances/get_user_profile/')
  },

  getUserByTelegramId(telegramId) {
    return api.get(`/users/by_telegram/${telegramId}/`)
  },

  getUserCardsByTelegramId(telegramId) {
    return api.get('/cards/instances/', {
      params: { telegram_id: telegramId }
    })
  }
}
