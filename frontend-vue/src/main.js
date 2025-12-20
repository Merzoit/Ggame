import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'
import api from './services/api'

// Инициализация Telegram WebApp
function initTelegramWebApp() {
  if (window.Telegram?.WebApp) {
    const webApp = window.Telegram.WebApp

    // Разрешаем закрытие WebApp
    webApp.ready()
    webApp.expand()

    // Получаем данные пользователя
    const initData = webApp.initDataUnsafe
    if (initData?.user) {
      const telegramId = initData.user.id

      // Сохраняем telegramId для использования в API
      localStorage.setItem('telegram_user_id', telegramId)

      // Для тестирования - создаем токен на основе telegramId
      const testToken = `test_token_${telegramId}`
      localStorage.setItem('ggame_token', testToken)
    } else {
      // Для тестирования в браузере без Telegram
      const testToken = 'test_token_123456789'
      localStorage.setItem('ggame_token', testToken)
      localStorage.setItem('telegram_user_id', '123456789')
    }

    // Настраиваем цвета WebApp
    webApp.setHeaderColor('#141420')
    webApp.setBackgroundColor('#0a0a0f')
  } else {
    // Для тестирования в браузере без Telegram
    const testToken = 'test_token_123456789'
    localStorage.setItem('ggame_token', testToken)
    localStorage.setItem('telegram_user_id', '123456789')
  }
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Инициализируем Telegram WebApp
initTelegramWebApp()

app.mount('#app')