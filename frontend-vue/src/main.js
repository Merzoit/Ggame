import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'
import api from './services/api'

// Инициализация Telegram WebApp
function initTelegramWebApp() {
  console.log('🎮 Initializing Telegram WebApp...')

  // Проверяем URL параметры для тестирования (например: ?test_user=123456789)
  const urlParams = new URLSearchParams(window.location.search)
  const testUserId = urlParams.get('test_user')

  if (window.Telegram?.WebApp) {
    console.log('✅ Telegram WebApp detected')
    const webApp = window.Telegram.WebApp

    // Разрешаем закрытие WebApp
    webApp.ready()
    webApp.expand()

    // Получаем данные пользователя
    const initData = webApp.initDataUnsafe
    console.log('📊 Init data:', initData)

    if (initData?.user) {
      const telegramId = initData.user.id
      console.log('👤 User ID:', telegramId)

      // Сохраняем telegramId для использования в API
      localStorage.setItem('telegram_user_id', telegramId)

      // Для тестирования - создаем токен на основе telegramId
      const testToken = `test_token_${telegramId}`
      localStorage.setItem('ggame_token', testToken)
      console.log('🔑 Token set:', testToken)
    } else {
      console.log('⚠️ No user data in initData - using test mode')
      setupTestUser()
    }

    // Настраиваем цвета WebApp
    webApp.setHeaderColor('#141420')
    webApp.setBackgroundColor('#0a0a0f')
  } else {
    console.log('⚠️ Telegram WebApp not detected - browser test mode')
    setupTestUser()
  }

  console.log('🎮 Telegram WebApp initialization completed')
}

// Настройка тестового пользователя
function setupTestUser() {
  // Если указан test_user в URL, используем его
  const urlParams = new URLSearchParams(window.location.search)
  const testUserId = urlParams.get('test_user') || '123456789'

  console.log('🎭 Setting up test user:', testUserId)
  localStorage.setItem('telegram_user_id', testUserId)
  localStorage.setItem('ggame_token', `test_token_${testUserId}`)
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Инициализируем Telegram WebApp
initTelegramWebApp()

app.mount('#app')