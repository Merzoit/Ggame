// Компоненты интерфейса GGame

class GGameComponents {
    constructor() {
        this.modals = [];
        this.toasts = [];
    }

    // Создание toast уведомлений
    showToast(message, type = 'info', duration = CONFIG.UI.TOAST_DURATION) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${message}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Добавление стилей для toast
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--card-bg);
            border-radius: var(--radius-md);
            padding: var(--spacing-md);
            box-shadow: var(--shadow-lg);
            z-index: 10000;
            max-width: 300px;
            animation: slideInRight 0.3s ease;
            border-left: 4px solid ${this.getToastColor(type)};
        `;

        document.body.appendChild(toast);
        this.toasts.push(toast);

        // Автоматическое удаление
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, duration);
    }

    getToastColor(type) {
        const colors = {
            success: 'var(--success-color)',
            error: 'var(--error-color)',
            warning: 'var(--warning-color)',
            info: 'var(--primary-color)'
        };
        return colors[type] || colors.info;
    }

    // Создание модальных окон
    createModal(title, content, options = {}) {
        const modalId = `modal-${Date.now()}`;
        const modal = document.createElement('div');
        modal.className = 'modal-backdrop';
        modal.id = modalId;
        modal.innerHTML = `
            <div class="modal-content">
                <button class="modal-close" onclick="components.closeModal('${modalId}')">×</button>
                ${title ? `<h3 class="modal-title">${title}</h3>` : ''}
                <div class="modal-body">
                    ${content}
                </div>
                ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
            </div>
        `;

        document.getElementById('modals-container').appendChild(modal);
        this.modals.push(modalId);

        // Закрытие по клику на backdrop
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal(modalId);
            }
        });

        return modalId;
    }

    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => modal.remove(), 300);
            this.modals = this.modals.filter(id => id !== modalId);
        }
    }

    closeAllModals() {
        this.modals.forEach(modalId => this.closeModal(modalId));
    }

    // Создание карточки карты
    createCardElement(cardData, options = {}) {
        const card = document.createElement('div');
        card.className = `deck-card ${options.selected ? 'selected' : ''}`;
        card.dataset.cardId = cardData.id;

        const element = CONFIG.ELEMENTS[cardData.template?.element] || CONFIG.ELEMENTS.neutral;

        card.innerHTML = `
            <div class="card-header">
                <div class="card-name">${cardData.template?.name || cardData.name}</div>
                <div class="card-element" style="background: ${element.color}20; color: ${element.color}">
                    ${element.icon}
                </div>
            </div>
            <div class="card-stats">
                <div class="card-stat">
                    <span class="card-stat-value">${cardData.health || cardData.template?.health_min}</span>
                    <div class="card-stat-label">HP</div>
                </div>
                <div class="card-stat">
                    <span class="card-stat-value">${cardData.attack || cardData.template?.attack_min}</span>
                    <div class="card-stat-label">ATK</div>
                </div>
                <div class="card-stat">
                    <span class="card-stat-value">${cardData.defense || cardData.template?.defense_min}</span>
                    <div class="card-stat-label">DEF</div>
                </div>
            </div>
        `;

        if (options.clickable) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', () => {
                if (options.onClick) options.onClick(cardData);
            });
        }

        return card;
    }

    // Создание элемента инвентаря
    createInventoryItemElement(itemData, options = {}) {
        const item = document.createElement('div');
        item.className = 'inventory-item';
        item.dataset.itemId = itemData.id;

        item.innerHTML = `
            <div class="item-icon">${this.getItemIcon(itemData)}</div>
            <div class="item-name">${itemData.name}</div>
            ${itemData.quantity > 1 ? `<div class="item-quantity">${itemData.quantity}</div>` : ''}
        `;

        if (options.clickable) {
            item.addEventListener('click', () => {
                if (options.onClick) options.onClick(itemData);
            });
        }

        return item;
    }

    getItemIcon(item) {
        // Простая логика для иконок предметов
        const icons = {
            'consumable': '🧪',
            'equipment': '⚔️',
            'collectible': '🏆',
            'currency': '💰'
        };
        return icons[item.item_type] || '📦';
    }

    // Создание товара в магазине
    createShopItemElement(itemData, options = {}) {
        const item = document.createElement('div');
        item.className = 'shop-item';
        item.dataset.itemId = itemData.id;

        item.innerHTML = `
            <div class="shop-item-image">${this.getItemIcon(itemData)}</div>
            <div class="shop-item-name">${itemData.name}</div>
            <div class="shop-item-price">
                <span class="currency-icon">${itemData.coin_cost > 0 ? '🪙' : '💰'}</span>
                <span>${itemData.coin_cost || itemData.gold_cost}</span>
            </div>
            <button class="shop-buy-btn">Купить</button>
        `;

        const buyBtn = item.querySelector('.shop-buy-btn');
        buyBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (options.onBuy) options.onBuy(itemData);
        });

        if (options.clickable) {
            item.addEventListener('click', () => {
                if (options.onClick) options.onClick(itemData);
            });
        }

        return item;
    }

    // Loading состояния
    showLoading() {
        const loader = document.getElementById('loading-screen');
        if (loader) loader.style.display = 'flex';
    }

    hideLoading() {
        const loader = document.getElementById('loading-screen');
        if (loader) loader.style.display = 'none';
    }

    // Управление состояниями загрузки для элементов
    setLoading(element, loading = true) {
        if (loading) {
            element.classList.add('loading');
            element.style.opacity = '0.6';
            element.style.pointerEvents = 'none';
        } else {
            element.classList.remove('loading');
            element.style.opacity = '';
            element.style.pointerEvents = '';
        }
    }

    // Анимации
    animate(element, animation, duration = 300) {
        element.style.animation = `${animation} ${duration}ms ease`;
        setTimeout(() => {
            element.style.animation = '';
        }, duration);
    }

    // Утилиты для работы с DOM
    $(selector) {
        return document.querySelector(selector);
    }

    $$(selector) {
        return document.querySelectorAll(selector);
    }

    createElement(tag, classes = '', content = '') {
        const element = document.createElement(tag);
        if (classes) element.className = classes;
        if (content) element.innerHTML = content;
        return element;
    }
}

// Создание экземпляра компонентов
const components = new GGameComponents();

// Экспорт для глобального использования
window.GGameComponents = GGameComponents;
window.components = components;
