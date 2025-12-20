import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/styles/main.css'
import api from './services/api'

// Инициализация Telegram WebApp
function initTelegramWebApp() {
  console.log('🎮 Initializing Telegram WebApp...')
  console.log('📱 UserAgent:', navigator.userAgent)
  console.log('🌐 Location:', window.location.href)
  console.log('🔧 Telegram object:', window.Telegram)
  console.log('🔧 window.Telegram.WebApp:', window.Telegram?.WebApp)

  // Проверяем URL параметры для тестирования (например: ?test_user=123456789)
  const urlParams = new URLSearchParams(window.location.search)
  const testUserId = urlParams.get('test_user')
  const userId = urlParams.get('user_id')
  console.log('🎯 URL test_user param:', testUserId)
  console.log('🎯 URL user_id param:', userId)

  // Проверяем tgWebAppData в URL
  const tgWebAppData = urlParams.get('tgWebAppData')
  console.log('🎯 tgWebAppData present:', !!tgWebAppData)

  if (tgWebAppData) {
    console.log('📊 Parsing tgWebAppData...')
    try {
      // Парсим tgWebAppData для получения user данных
      const decodedData = decodeURIComponent(tgWebAppData)
      console.log('📊 Decoded tgWebAppData:', decodedData)

      // Ищем user данные в decoded string
      const userMatch = decodedData.match(/user%3D(%7B[^%]*%7D)/)
      if (userMatch) {
        const userJson = decodeURIComponent(userMatch[1])
        const userData = JSON.parse(userJson)
        console.log('👤 Parsed user data:', userData)

        const telegramId = userData.id.toString()
        console.log('👤 Telegram ID from URL:', telegramId)

        // Сохраняем telegramId для использования в API
        localStorage.setItem('telegram_user_id', telegramId)
        localStorage.setItem('ggame_token', `tg_token_${telegramId}`)
        console.log('💾 Saved to localStorage: telegram_user_id =', telegramId)

        // Показываем данные в UI
        window.telegramUserId = telegramId
        return // Выходим, так как успешно обработали
      }
    } catch (e) {
      console.error('❌ Error parsing tgWebAppData:', e)
    }
  }

  // Если tgWebAppData не найден или не удалось распарсить, используем user_id или test_user
  if (userId) {
    console.log('👤 Using user_id from URL:', userId)
    localStorage.setItem('telegram_user_id', userId)
    localStorage.setItem('ggame_token', `tg_token_${userId}`)
    window.telegramUserId = userId
    return
  }

  // Если WebApp данные уже обработаны из URL, ничего не делаем
  if (window.telegramUserId) {
    console.log('✅ Telegram user already initialized from URL:', window.telegramUserId)
    return
  }

  if (window.Telegram?.WebApp) {
    console.log('✅ Telegram WebApp detected')
    const webApp = window.Telegram.WebApp
    console.log('📋 WebApp object:', webApp)

    try {
      // Разрешаем закрытие WebApp
      webApp.ready()
      webApp.expand()
      console.log('✅ WebApp ready and expanded')
    } catch (e) {
      console.error('❌ Error initializing WebApp:', e)
    }

    // Получаем данные пользователя
    const initData = webApp.initDataUnsafe
    console.log('📊 Init data:', initData)
    console.log('📊 Init data user:', initData?.user)

    if (initData?.user) {
      const telegramId = initData.user.id
      console.log('👤 User ID from WebApp:', telegramId)

      // Сохраняем telegramId для использования в API
      localStorage.setItem('telegram_user_id', telegramId)
      console.log('💾 Saved to localStorage: telegram_user_id =', telegramId)

      // Для тестирования - создаем токен на основе telegramId
      const testToken = `test_token_${telegramId}`
      localStorage.setItem('ggame_token', testToken)
      console.log('🔑 Token set:', testToken)

      // Показываем данные в UI
      window.telegramUserId = telegramId
      console.log('🌐 window.telegramUserId set to:', telegramId)
    } else {
      console.log('⚠️ No user data in WebApp initData - using test mode')
      setupTestUser()
    }

    // Настраиваем цвета WebApp
    try {
      webApp.setHeaderColor('#141420')
      webApp.setBackgroundColor('#0a0a0f')
      console.log('🎨 WebApp colors set')
    } catch (e) {
      console.error('❌ Error setting WebApp colors:', e)
    }
  } else {
    console.log('⚠️ Telegram WebApp not detected - using test mode')
    setupTestUser()
  }

  console.log('🎮 Telegram WebApp initialization completed')

  // Запускаем тестовый API запрос через 2 секунды
  setTimeout(() => {
    console.log('🚀 Starting test API call...')
    testApiCall()
  }, 2000)
}

// Тестовый API вызов
async function testApiCall() {
  try {
    console.log('📡 Making test API call to get_user_profile')
    const telegramId = localStorage.getItem('telegram_user_id') || '680756851'
    console.log('🆔 Using telegram_id:', telegramId)

    const response = await fetch(`https://web-production-051b.up.railway.app/api/cards/instances/get_user_profile/?telegram_id=${telegramId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    console.log('📨 API Response status:', response.status)
    console.log('📨 API Response headers:', Object.fromEntries(response.headers.entries()))

    const data = await response.text()
    console.log('📄 API Response data:', data.substring(0, 500))

  } catch (error) {
    console.error('❌ API call failed:', error)
  }
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