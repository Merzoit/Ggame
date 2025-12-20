# Скрипт для тестирования живого API

$RAILWAY_URL = "https://web-production-051b.up.railway.app"
$VERCEL_URL = "https://ggame-psi.vercel.app"

Write-Host "🧪 Тестирование живого API..." -ForegroundColor Green
Write-Host "Railway: $RAILWAY_URL" -ForegroundColor Blue
Write-Host "Vercel: $VERCEL_URL" -ForegroundColor Blue
Write-Host ""

# 1. Тест API доступности
Write-Host "1. Тест API доступности..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$RAILWAY_URL/api/telegram/test/" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json
        Write-Host "   [OK] API доступен: $($data.message)" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] Статус: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   [ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Тест главной страницы фронтенда
Write-Host "2. Тест фронтенда..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri $VERCEL_URL -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "   [OK] Фронтенд доступен" -ForegroundColor Green
        if ($response.Content -match "vue") {
            Write-Host "   [OK] Найден Vue.js" -ForegroundColor Green
        } else {
            Write-Host "   [WARNING] Vue.js не найден" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   [ERROR] Статус: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   [ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 3. Тест страницы профиля
Write-Host "3. Тест страницы профиля..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$VERCEL_URL/#/profile" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "   [OK] Страница профиля доступна" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] Статус: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   [ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 4. Тест админки
Write-Host "4. Тест админки..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$RAILWAY_URL/admin/" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "   [OK] Админка доступна" -ForegroundColor Green
        if ($response.Content -match "Django") {
            Write-Host "   [OK] Django админка загружена" -ForegroundColor Green
        }
        # Проверяем CSS
        if ($response.Content -match "admin/css") {
            Write-Host "   [OK] CSS ссылки найдены" -ForegroundColor Green
        } else {
            Write-Host "   [WARNING] CSS ссылки не найдены" -ForegroundColor Yellow
        }
    } elseif ($response.StatusCode -eq 302) {
        Write-Host "   [OK] Редирект на логин (нормально)" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] Статус: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   [ERROR] $($_.Exception.Message)" -ForegroundColor Red
}

# 5. Тест статических файлов
Write-Host "5. Тест статических файлов..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$RAILWAY_URL/static/admin/css/base.css" -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "   [OK] CSS файл доступен" -ForegroundColor Green
    } else {
        Write-Host "   [ERROR] CSS файл не найден: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   [ERROR] CSS файл недоступен: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Инструкции:" -ForegroundColor Cyan
Write-Host "1. Настройте переменные окружения в Railway (см. RAILWAY_SETUP.md)" -ForegroundColor White
Write-Host "2. Подождите передеплой Railway (2-3 минуты)" -ForegroundColor White
Write-Host "3. Напишите /start боту @MerzoitCodeBot" -ForegroundColor White
Write-Host "4. Нажмите 'Начать игру'" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Ожидаемый результат:" -ForegroundColor Green
Write-Host "   Бот откроет: https://ggame-psi.vercel.app/#/profile?user_id=ВАШ_ID" -ForegroundColor White
Write-Host ""
Write-Host "✅ Готово!" -ForegroundColor Green
