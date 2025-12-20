# Скрипт для тестирования webhook в Railway

param(
    [string]$RailwayUrl = "",
    [switch]$Help
)

if ($Help -or -not $RailwayUrl) {
    Write-Host "Скрипт для тестирования Telegram webhook в Railway" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Использование:" -ForegroundColor Yellow
    Write-Host "  .\test_webhook_railway.ps1 -RailwayUrl 'https://your-app.railway.app'" -ForegroundColor White
    Write-Host ""
    Write-Host "Пример:" -ForegroundColor Green
    Write-Host "  .\test_webhook_railway.ps1 -RailwayUrl 'https://ggame-production.up.railway.app'" -ForegroundColor White
    Write-Host ""
    Write-Host "Что проверяет:" -ForegroundColor Cyan
    Write-Host "  ✅ Доступность API эндпоинтов" -ForegroundColor White
    Write-Host "  ✅ Статус webhook бота" -ForegroundColor White
    Write-Host "  ✅ Переменные окружения" -ForegroundColor White
    exit 0
}

Write-Host "🔍 Тестирование Railway webhook..." -ForegroundColor Green
Write-Host "URL: $RailwayUrl" -ForegroundColor Blue
Write-Host ""

# 1. Проверка доступности API
Write-Host "1️⃣ Проверка API доступности..." -ForegroundColor Yellow
try {
    $apiUrl = "$RailwayUrl/api/telegram/test/"
    $response = Invoke-WebRequest -Uri $apiUrl -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "  ✅ API доступен" -ForegroundColor Green
        $apiData = $response.Content | ConvertFrom-Json
        Write-Host "  📄 Ответ: $($apiData.message)" -ForegroundColor Gray
    } else {
        Write-Host "  ❌ API вернул статус $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "  ❌ Ошибка доступа к API: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 2. Проверка webhook статуса
Write-Host "2️⃣ Проверка статуса webhook..." -ForegroundColor Yellow
try {
    python manage.py webhook_status
} catch {
    Write-Host "  ❌ Ошибка проверки webhook: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 3. Тестирование отправки сообщения
Write-Host "3️⃣ Тестирование отправки сообщения..." -ForegroundColor Yellow
$chatId = Read-Host "Введите ваш Telegram Chat ID (или нажмите Enter для пропуска)"
if ($chatId) {
    try {
        python manage.py test_bot --chat-id $chatId
    } catch {
        Write-Host "  ❌ Ошибка отправки тестового сообщения: $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "  ⏭️  Пропущено (нужен Chat ID)" -ForegroundColor Gray
}

Write-Host ""

# 4. Инструкции
Write-Host "📋 Следующие шаги:" -ForegroundColor Cyan
Write-Host ""
Write-Host "Если API недоступен:" -ForegroundColor Yellow
Write-Host "  • Проверьте логи Railway (Deployments > View Logs)" -ForegroundColor White
Write-Host "  • Убедитесь, что сервис запущен" -ForegroundColor White
Write-Host ""
Write-Host "Если webhook не установлен:" -ForegroundColor Yellow
Write-Host "  • Проверьте переменные окружения в Railway" -ForegroundColor White
Write-Host "  • Перезапустите сервис" -ForegroundColor White
Write-Host "  • Или выполните: python manage.py setup_bot" -ForegroundColor White
Write-Host ""
Write-Host "Для получения Chat ID:" -ForegroundColor Yellow
Write-Host "  • Напишите боту @userinfobot" -ForegroundColor White
Write-Host "  • Он пришлет ваш Chat ID" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Готово!" -ForegroundColor Green
