import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor для добавления токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('ggame_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
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

  removeCardFromDeck(position) {
    return api.post('/cards/decks/remove_card/', {
      position
    })
  },

  // Cards endpoints
  getCardTemplates(params = {}) {
    return api.get('/cards/templates/', { params })
  },

  getUserCards() {
    return api.get('/cards/instances/')
  },

  acquireCard(templateId) {
    return api.post('/cards/instances/acquire_card/', {
      template_id: templateId
    })
  },

  sellCard(cardId) {
    return api.post(`/cards/instances/${cardId}/sell_card/`)
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
    return api.get('/cards/universes/')
  },

  getSeasons(universeId = null) {
    const params = universeId ? { universe: universeId } : {}
    return api.get('/cards/seasons/', { params })
  }
}
