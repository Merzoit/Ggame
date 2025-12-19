// Основной JavaScript файл GGame

class GGameApp {
    constructor() {
        this.currentSection = 'deck';
        this.user = null;
        this.deck = null;
        this.inventory = [];
        this.cardTemplates = [];
        this.initialized = false;

        this.init();
    }

    async init() {
        try {
            // Показать загрузку
            components.showLoading();

            // Инициализация приложения
            await this.initializeApp();

            // Настройка обработчиков событий
            this.setupEventListeners();

            // Загрузка данных
            await this.loadUserData();
            await this.loadDeckData();
            await this.loadInventoryData();

            // Скрыть загрузку
            components.hideLoading();

            this.initialized = true;
            console.log('GGame initialized successfully');

        } catch (error) {
            console.error('Failed to initialize GGame:', error);
            components.showToast(CONFIG.MESSAGES.ERROR_SERVER, 'error');
            components.hideLoading();
        }
    }

    async initializeApp() {
        // Проверка Telegram WebApp
        if (TelegramWebApp) {
            console.log('Running in Telegram WebApp');

            // Получение данных пользователя из Telegram
            if (TelegramWebApp.initDataUnsafe?.user) {
                this.user = TelegramWebApp.initDataUnsafe.user;
                this.updateUserUI(this.user);
            }
        } else {
            console.log('Running in browser');

            // Для разработки - моковые данные
            this.user = {
                id: 1,
                username: 'Player',
                coins: 100,
                gold: 5,
                games_won: 12
            };
            this.updateUserUI(this.user);
        }

        // Установка токена (если есть)
        const token = localStorage.getItem('ggame_token');
        if (token) {
            api.setToken(token);
        }
    }

    setupEventListeners() {
        // Навигация
        const navItems = components.$$('.nav-item, .bottom-nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                this.switchSection(section);
            });
        });

        // Кнопки в разделах
        const editDeckBtn = components.$('#edit-deck-btn');
        if (editDeckBtn) {
            editDeckBtn.addEventListener('click', () => this.toggleDeckEditMode());
        }

        // Фильтры
        const inventoryFilter = components.$('#inventory-filter');
        if (inventoryFilter) {
            inventoryFilter.addEventListener('change', (e) => this.filterInventory(e.target.value));
        }

        // Поиск в базе знаний
        const knowledgeSearch = components.$('#knowledge-search');
        if (knowledgeSearch) {
            knowledgeSearch.addEventListener('input', (e) => this.searchKnowledge(e.target.value));
        }

        // Категории базы знаний
        const knowledgeCategories = components.$$('.category-card');
        knowledgeCategories.forEach(category => {
            category.addEventListener('click', () => {
                const categoryType = category.dataset.category;
                this.showKnowledgeCategory(categoryType);
            });
        });

        // Табы магазина
        const shopTabs = components.$$('.tab-btn');
        shopTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const tabName = tab.dataset.tab;
                this.switchShopTab(tabName);
            });
        });
    }

    switchSection(sectionName) {
        // Скрыть текущий раздел
        const currentSection = components.$(`#${this.currentSection}-section`);
        if (currentSection) {
            currentSection.classList.remove('active');
        }

        // Показать новый раздел
        const newSection = components.$(`#${sectionName}-section`);
        if (newSection) {
            newSection.classList.add('active');
        }

        // Обновить активную навигацию
        components.$$('.nav-item, .bottom-nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.section === sectionName);
        });

        this.currentSection = sectionName;

        // Загрузка данных для раздела
        this.loadSectionData(sectionName);
    }

    async loadSectionData(sectionName) {
        switch (sectionName) {
            case 'deck':
                await this.loadDeckData();
                break;
            case 'inventory':
                await this.loadInventoryData();
                break;
            case 'shop':
                await this.loadShopData();
                break;
        }
    }

    async loadUserData() {
        try {
            // Загрузка данных пользователя
            // В реальном приложении - запрос к API
            console.log('Loading user data...');
        } catch (error) {
            console.error('Failed to load user data:', error);
        }
    }

    async loadDeckData() {
        try {
            // Загрузка данных колоды
            const response = await api.getDeck();
            this.deck = response;
            this.updateDeckUI();
        } catch (error) {
            console.error('Failed to load deck data:', error);
            // Для разработки - моковые данные
            this.deck = {
                name: 'Моя колода',
                cards_count: 0,
                total_stats: { health: 0, attack: 0, defense: 0 },
                is_valid_deck: { valid: false, message: 'Нужно 3 карты' },
                cards: []
            };
            this.updateDeckUI();
        }
    }

    async loadInventoryData() {
        try {
            // Загрузка инвентаря
            const response = await api.getInventory();
            this.inventory = response.results || response;
            this.updateInventoryUI();
        } catch (error) {
            console.error('Failed to load inventory data:', error);
            // Для разработки - моковые данные
            this.inventory = [];
            this.updateInventoryUI();
        }
    }

    async loadShopData() {
        try {
            // Загрузка данных магазина
            const templates = await api.getCardTemplates();
            this.cardTemplates = templates.results || templates;
            this.updateShopUI();
        } catch (error) {
            console.error('Failed to load shop data:', error);
        }
    }

    updateUserUI(userData) {
        // Обновление UI пользователя
        const username = components.$('#username');
        const userLevel = components.$('#user-level');
        const userWins = components.$('#user-wins');
        const coinsAmount = components.$('#coins-amount');
        const goldAmount = components.$('#gold-amount');

        if (username) username.textContent = userData.username || userData.first_name || 'Игрок';
        if (userLevel) userLevel.textContent = Math.floor(userData.games_won / 10) + 1 || 1;
        if (userWins) userWins.textContent = userData.games_won || 0;
        if (coinsAmount) coinsAmount.textContent = userData.coins || 0;
        if (goldAmount) goldAmount.textContent = userData.gold || 0;
    }

    updateDeckUI() {
        if (!this.deck) return;

        // Обновление статистики колоды
        const healthEl = components.$('#deck-health');
        const attackEl = components.$('#deck-attack');
        const defenseEl = components.$('#deck-defense');

        if (healthEl) healthEl.textContent = this.deck.total_stats?.health || 0;
        if (attackEl) attackEl.textContent = this.deck.total_stats?.attack || 0;
        if (defenseEl) defenseEl.textContent = this.deck.total_stats?.defense || 0;

        // Обновление сетки карт
        const deckGrid = components.$('#deck-grid');
        if (deckGrid) {
            deckGrid.innerHTML = '';

            // Добавление карт колоды
            if (this.deck.cards && this.deck.cards.length > 0) {
                this.deck.cards.forEach(cardData => {
                    const cardElement = components.createCardElement(cardData.card_info || cardData);
                    deckGrid.appendChild(cardElement);
                });
            }

            // Добавление пустых слотов
            const emptySlots = 3 - (this.deck.cards?.length || 0);
            for (let i = 0; i < emptySlots; i++) {
                const emptySlot = components.createElement('div', 'empty-slot');
                emptySlot.innerHTML = `
                    <div class="empty-slot-icon">➕</div>
                    <div class="empty-slot-text">Добавить карту</div>
                `;
                emptySlot.addEventListener('click', () => this.showAddCardModal());
                deckGrid.appendChild(emptySlot);
            }
        }
    }

    updateInventoryUI() {
        const inventoryGrid = components.$('#inventory-grid');
        if (inventoryGrid) {
            inventoryGrid.innerHTML = '';

            if (this.inventory.length === 0) {
                const emptyState = components.createElement('div', 'empty-state');
                emptyState.innerHTML = `
                    <div class="empty-icon">🎒</div>
                    <div class="empty-title">Инвентарь пуст</div>
                    <div class="empty-text">Здесь появятся ваши предметы</div>
                `;
                inventoryGrid.appendChild(emptyState);
            } else {
                this.inventory.forEach(item => {
                    const itemElement = components.createInventoryItemElement(item, {
                        clickable: true,
                        onClick: (itemData) => this.showItemModal(itemData)
                    });
                    inventoryGrid.appendChild(itemElement);
                });
            }
        }
    }

    updateShopUI() {
        const cardsGrid = components.$('#cards-shop-grid');
        if (cardsGrid && this.cardTemplates.length > 0) {
            cardsGrid.innerHTML = '';

            this.cardTemplates.slice(0, 12).forEach(template => {
                const shopItem = components.createShopItemElement(template, {
                    onBuy: (itemData) => this.buyCard(itemData)
                });
                cardsGrid.appendChild(shopItem);
            });
        }
    }

    // Методы для работы с колодой
    toggleDeckEditMode() {
        const editMode = !document.body.classList.contains('deck-edit-mode');
        document.body.classList.toggle('deck-edit-mode');

        const editBtn = components.$('#edit-deck-btn');
        if (editBtn) {
            editBtn.innerHTML = editMode ?
                '<span class="btn-icon">💾</span>Сохранить' :
                '<span class="btn-icon">✏️</span>Редактировать';
        }

        components.showToast(
            editMode ? 'Режим редактирования включен' : 'Изменения сохранены',
            editMode ? 'info' : 'success'
        );
    }

    showAddCardModal() {
        // Модальное окно для выбора карты из инвентаря
        const content = `
            <div class="card-selection">
                <h4>Выберите карту для добавления</h4>
                <div class="available-cards" id="available-cards">
                    <!-- Карты будут загружены здесь -->
                </div>
            </div>
        `;

        const modalId = components.createModal('Добавить карту', content, {
            footer: '<button class="action-btn secondary" onclick="components.closeModal(\'' + modalId + '\')">Отмена</button>'
        });

        // Загрузка доступных карт (тех, что есть у игрока, но не в колоде)
        this.loadAvailableCards(modalId);
    }

    async loadAvailableCards(modalId) {
        try {
            const userCards = await api.getUserCards();
            const availableCards = userCards.filter(card => !card.is_in_deck);

            const container = components.$(`#${modalId} #available-cards`);
            if (container) {
                container.innerHTML = '';

                if (availableCards.length === 0) {
                    container.innerHTML = '<p>Нет доступных карт для добавления</p>';
                } else {
                    availableCards.forEach(card => {
                        const cardElement = components.createCardElement(card, {
                            clickable: true,
                            onClick: (cardData) => this.selectCardForDeck(cardData, modalId)
                        });
                        container.appendChild(cardElement);
                    });
                }
            }
        } catch (error) {
            console.error('Failed to load available cards:', error);
        }
    }

    async selectCardForDeck(cardData, modalId) {
        // Показать выбор позиции
        const positionSelector = `
            <div class="position-selector">
                <h4>Выберите позицию для карты "${cardData.template?.name}"</h4>
                <div class="position-grid">
                    <button class="position-btn" data-position="1">Позиция 1</button>
                    <button class="position-btn" data-position="2">Позиция 2</button>
                    <button class="position-btn" data-position="3">Позиция 3</button>
                </div>
            </div>
        `;

        // Обновить модальное окно
        const modalContent = components.$(`#${modalId} .modal-body`);
        if (modalContent) {
            modalContent.innerHTML = positionSelector;

            // Обработчики для позиций
            const positionBtns = modalContent.querySelectorAll('.position-btn');
            positionBtns.forEach(btn => {
                btn.addEventListener('click', async () => {
                    const position = parseInt(btn.dataset.position);
                    await this.addCardToDeck(cardData.id, position);
                    components.closeModal(modalId);
                });
            });
        }
    }

    async addCardToDeck(cardId, position) {
        try {
            await api.addCardToDeck(cardId, position);
            await this.loadDeckData();
            components.showToast('Карта добавлена в колоду', 'success');
        } catch (error) {
            console.error('Failed to add card to deck:', error);
            components.showToast('Не удалось добавить карту', 'error');
        }
    }

    // Методы для магазина
    async buyCard(cardTemplate) {
        try {
            await api.acquireCard(cardTemplate.id);
            components.showToast(`Карта "${cardTemplate.name}" куплена!`, 'success');
            await this.loadUserData(); // Обновить валюту
            await this.loadDeckData(); // Обновить колоду
        } catch (error) {
            console.error('Failed to buy card:', error);
            components.showToast('Не удалось купить карту', 'error');
        }
    }

    // Методы для фильтрации
    filterInventory(filterType) {
        const inventoryGrid = components.$('#inventory-grid');
        const items = inventoryGrid.querySelectorAll('.inventory-item');

        items.forEach(item => {
            const itemType = item.dataset.itemType;
            if (filterType === 'all' || itemType === filterType) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }

    // Методы для базы знаний
    searchKnowledge(query) {
        // Простая логика поиска
        const categories = components.$$('.category-card');
        categories.forEach(category => {
            const title = category.querySelector('.category-title').textContent.toLowerCase();
            const description = category.querySelector('.category-description').textContent.toLowerCase();
            const matches = title.includes(query.toLowerCase()) || description.includes(query.toLowerCase());
            category.style.display = matches || query === '' ? 'block' : 'none';
        });
    }

    showKnowledgeCategory(categoryType) {
        const article = components.$('#knowledge-article');
        if (article) {
            const content = this.getKnowledgeContent(categoryType);
            article.innerHTML = `<div class="knowledge-article-content">${content}</div>`;
        }
    }

    getKnowledgeContent(categoryType) {
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
        };
        return content[categoryType] || '<p>Информация по этой категории готовится...</p>';
    }

    // Методы для табов магазина
    switchShopTab(tabName) {
        // Скрыть все табы
        components.$$('.shop-tab').forEach(tab => tab.classList.remove('active'));

        // Показать выбранный таб
        const selectedTab = components.$(`#${tabName}-tab`);
        if (selectedTab) selectedTab.classList.add('active');

        // Обновить активные кнопки табов
        components.$$('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabName);
        });
    }

    // Модальные окна для предметов
    showItemModal(itemData) {
        const content = `
            <div class="item-details">
                <div class="item-header">
                    <div class="item-icon-large">${components.getItemIcon(itemData)}</div>
                    <div class="item-info">
                        <h3>${itemData.name}</h3>
                        <p class="item-description">${itemData.description || 'Нет описания'}</p>
                    </div>
                </div>
                <div class="item-stats">
                    <div class="stat-row">
                        <span>Количество:</span>
                        <span>${itemData.quantity || 1}</span>
                    </div>
                    <div class="stat-row">
                        <span>Тип:</span>
                        <span>${this.getItemTypeName(itemData.item_type)}</span>
                    </div>
                </div>
                <div class="item-actions">
                    <button class="action-btn primary" onclick="app.useItem(${itemData.id})">Использовать</button>
                    <button class="action-btn secondary" onclick="components.closeAllModals()">Закрыть</button>
                </div>
            </div>
        `;

        components.createModal('Предмет', content);
    }

    getItemTypeName(type) {
        const types = {
            'consumable': 'Расходуемый',
            'equipment': 'Экипировка',
            'collectible': 'Коллекционный',
            'currency': 'Валюта'
        };
        return types[type] || type;
    }

    async useItem(itemId) {
        // Логика использования предмета
        components.showToast('Функция использования предметов в разработке', 'info');
        components.closeAllModals();
    }
}

// Инициализация приложения
document.addEventListener('DOMContentLoaded', () => {
    window.app = new GGameApp();
});

// Обработка ошибок
window.addEventListener('error', (e) => {
    console.error('Application error:', e.error);
    components.showToast('Произошла ошибка в приложении', 'error');
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
    components.showToast('Произошла ошибка сети', 'error');
});
