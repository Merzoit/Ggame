// API модуль для работы с GGame бэкендом

class GGameAPI {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.token = null;
        this.user = null;
    }

    // Установка токена авторизации
    setToken(token) {
        this.token = token;
    }

    // Получение заголовков для запросов
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        return headers;
    }

    // Обработка ответа
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({ message: 'Network error' }));
            throw new Error(error.message || `HTTP ${response.status}`);
        }

        return response.json();
    }

    // GET запрос
    async get(endpoint, params = {}) {
        const url = new URL(this.baseURL + endpoint);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.append(key, params[key]);
            }
        });

        const response = await fetch(url, {
            method: 'GET',
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    // POST запрос
    async post(endpoint, data = {}) {
        const response = await fetch(this.baseURL + endpoint, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });

        return this.handleResponse(response);
    }

    // PUT запрос
    async put(endpoint, data = {}) {
        const response = await fetch(this.baseURL + endpoint, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });

        return this.handleResponse(response);
    }

    // PATCH запрос
    async patch(endpoint, data = {}) {
        const response = await fetch(this.baseURL + endpoint, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });

        return this.handleResponse(response);
    }

    // DELETE запрос
    async delete(endpoint) {
        const response = await fetch(this.baseURL + endpoint, {
            method: 'DELETE',
            headers: this.getHeaders(),
        });

        return this.handleResponse(response);
    }

    // Методы для работы с колодой
    async getDeck() {
        return this.get(CONFIG.ENDPOINTS.CARDS_DECK);
    }

    async updateDeck(data) {
        return this.put(CONFIG.ENDPOINTS.CARDS_DECK, data);
    }

    async addCardToDeck(cardId, position) {
        return this.post(CONFIG.ENDPOINTS.CARDS_DECK + 'add_card/', {
            card_id: cardId,
            position: position
        });
    }

    async removeCardFromDeck(position) {
        return this.post(CONFIG.ENDPOINTS.CARDS_DECK + 'remove_card/', {
            position: position
        });
    }

    // Методы для работы с картами
    async getCardTemplates(params = {}) {
        return this.get(CONFIG.ENDPOINTS.CARDS_TEMPLATES, params);
    }

    async getUserCards() {
        return this.get(CONFIG.ENDPOINTS.CARDS_INSTANCES);
    }

    async acquireCard(templateId) {
        return this.post(CONFIG.ENDPOINTS.CARDS_INSTANCES + 'acquire_card/', {
            template_id: templateId
        });
    }

    async sellCard(cardId) {
        return this.post(CONFIG.ENDPOINTS.CARDS_INSTANCES + `${cardId}/sell_card/`);
    }

    // Методы для работы с инвентарем
    async getInventory() {
        return this.get(CONFIG.ENDPOINTS.INVENTORY);
    }

    async getItems(params = {}) {
        return this.get(CONFIG.ENDPOINTS.ITEMS, params);
    }

    // Методы для работы с аниме-вселенными и сезонами
    async getAnimeUniverses() {
        return this.get(CONFIG.ENDPOINTS.CARDS_TEMPLATES.replace('templates', 'universes'));
    }

    async getSeasons(universeId = null) {
        const params = universeId ? { universe: universeId } : {};
        return this.get(CONFIG.ENDPOINTS.CARDS_TEMPLATES.replace('templates', 'seasons'), params);
    }
}

// Создание экземпляра API
const api = new GGameAPI(CONFIG.API_BASE_URL);

// Экспорт для использования в других модулях
window.GGameAPI = GGameAPI;
window.api = api;
