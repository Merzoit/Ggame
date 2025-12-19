// Конфигурация GGame Frontend

const CONFIG = {
    // API настройки
    API_BASE_URL: 'http://127.0.0.1:8000/api',

    // Endpoints
    ENDPOINTS: {
        // Пользователь
        USER_PROFILE: '/users/profile/',

        // Карты
        CARDS_TEMPLATES: '/cards/templates/',
        CARDS_INSTANCES: '/cards/instances/',
        CARDS_DECK: '/cards/decks/',

        // Инвентарь
        INVENTORY: '/inventory/inventory/',
        ITEMS: '/inventory/items/',

        // Магазин (пока не реализован в бэкенде)
        SHOP: '/shop/',

        // Telegram Webhook
        TELEGRAM_WEBHOOK: '/telegram/webhook/',
    },

    // Настройки игры
    GAME: {
        DECK_SIZE: 3,
        MAX_CARDS_IN_DECK: 3,
    },

    // UI настройки
    UI: {
        ANIMATION_DURATION: 300,
        TOAST_DURATION: 3000,
        MODAL_Z_INDEX: 1000,
    },

    // Сообщения
    MESSAGES: {
        LOADING: 'Загрузка...',
        ERROR_NETWORK: 'Ошибка сети. Проверьте подключение.',
        ERROR_SERVER: 'Ошибка сервера. Попробуйте позже.',
        SUCCESS_SAVE: 'Изменения сохранены!',
        CONFIRM_DELETE: 'Вы уверены, что хотите удалить это?',
    },

    // Элементы стихий (для отображения)
    ELEMENTS: {
        fire: { name: 'Огонь', color: '#ff4757', icon: '🔥' },
        water: { name: 'Вода', color: '#3742fa', icon: '💧' },
        earth: { name: 'Земля', color: '#2ed573', icon: '🌱' },
        air: { name: 'Воздух', color: '#ffa502', icon: '💨' },
        light: { name: 'Свет', color: '#ffd32a', icon: '✨' },
        dark: { name: 'Тьма', color: '#7c5cbf', icon: '🌑' },
        neutral: { name: 'Нейтральная', color: '#a4b0be', icon: '⚪' },
    },

    // Редкости карт
    RARITIES: {
        common: { name: 'Обычная', color: '#a4b0be' },
        rare: { name: 'Редкая', color: '#3742fa' },
        epic: { name: 'Эпическая', color: '#9c88ff' },
        legendary: { name: 'Легендарная', color: '#ffa502' },
        mythic: { name: 'Мифическая', color: '#ff4757' },
    },
};

// Глобальные переменные приложения
let APP_STATE = {
    currentUser: null,
    currentSection: 'deck',
    userDeck: null,
    userInventory: [],
    isLoading: false,
    modals: [],
};

// Telegram WebApp (если запущено из Telegram)
let TelegramWebApp = null;

if (typeof window !== 'undefined' && window.TelegramWebApp) {
    TelegramWebApp = window.TelegramWebApp;

    // Настройка темы Telegram
    if (TelegramWebApp.themeParams) {
        applyTelegramTheme(TelegramWebApp.themeParams);
    }
}

function applyTelegramTheme(themeParams) {
    // Применение темы Telegram к приложению
    const root = document.documentElement;

    if (themeParams.bg_color) {
        root.style.setProperty('--primary-bg', themeParams.bg_color);
    }

    if (themeParams.secondary_bg_color) {
        root.style.setProperty('--secondary-bg', themeParams.secondary_bg_color);
    }

    if (themeParams.accent_text_color) {
        root.style.setProperty('--primary-color', themeParams.accent_text_color);
    }

    if (themeParams.text_color) {
        root.style.setProperty('--text-primary', themeParams.text_color);
    }
}
