# Скрипт для проверки FRONTEND_URL и Vue.js приложения

param(
    [string]$FrontendUrl = "",
    [switch]$Help
)

if ($Help -or -not $FrontendUrl) {
    Write-Host "Скрипт для проверки Vue.js фронтенда" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Использование:" -ForegroundColor Yellow
    Write-Host "  .\check_frontend_url.ps1 -FrontendUrl 'https://your-vercel-app.vercel.app'" -ForegroundColor White
    Write-Host ""
    Write-Host "Пример:" -ForegroundColor Green
    Write-Host "  .\check_frontend_url.ps1 -FrontendUrl 'https://ggame.vercel.app'" -ForegroundColor White
    exit 0
}

Write-Host "🔍 Проверка Vue.js фронтенда..." -ForegroundColor Green
Write-Host "URL: $FrontendUrl" -ForegroundColor Blue
Write-Host ""

# 1. Проверка главной страницы
Write-Host "1. Проверка главной страницы..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $FrontendUrl -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "  OK Главная страница доступна" -ForegroundColor Green
        if ($response.Content -match "vue") {
            Write-Host "  OK Найден Vue.js контент" -ForegroundColor Green
        } else {
            Write-Host "  WARNING Vue.js контент не найден" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ERROR Статус $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "  ERROR $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Проверка страницы профиля
Write-Host "2. Проверка страницы профиля..." -ForegroundColor Yellow
$profileUrl = "$FrontendUrl/#/profile"
try {
    $response = Invoke-WebRequest -Uri $profileUrl -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "  OK Страница профиля доступна" -ForegroundColor Green
        if ($response.Content -match "profile" -or $response.Content -match "Profile") {
            Write-Host "  OK Найден контент профиля" -ForegroundColor Green
        } else {
            Write-Host "  WARNING Контент профиля не найден" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ERROR Статус $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "  ERROR $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Проверка API доступности
Write-Host "3. Проверка API доступности..." -ForegroundColor Yellow
if ($FrontendUrl -match "vercel\.app") {
    # Для Vercel проверяем API через переменные окружения
    Write-Host "  INFO Проверьте VITE_API_BASE_URL в Vercel" -ForegroundColor Blue
} else {
    Write-Host "  INFO Это не Vercel URL" -ForegroundColor Blue
}

Write-Host ""
Write-Host "Проблемы и решения:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Если открывается не Vue.js приложение:" -ForegroundColor Yellow
Write-Host "  - Проверьте FRONTEND_URL в Railway Variables" -ForegroundColor White
Write-Host "  - Убедитесь, что Vercel развернул frontend-vue папку" -ForegroundColor White
Write-Host "  - Проверьте настройки в Vercel (Root Directory: frontend-vue)" -ForegroundColor White
Write-Host ""
Write-Host "Если страница профиля не работает:" -ForegroundColor Yellow
Write-Host "  - Проверьте Vue Router в frontend-vue/src/router/index.js" -ForegroundColor White
Write-Host "  - Убедитесь, что есть маршрут /profile" -ForegroundColor White
Write-Host ""
Write-Host "Тестирование:" -ForegroundColor Green
Write-Host "  1. Откройте $FrontendUrl в браузере" -ForegroundColor White
Write-Host "  2. Должно загрузиться Vue.js приложение" -ForegroundColor White
Write-Host "  3. Перейдите на $profileUrl" -ForegroundColor White
Write-Host "  4. Должна открыться страница профиля" -ForegroundColor White
