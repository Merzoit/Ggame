# Скрипт для тестирования Telegram бота локально
# Использует ngrok для создания туннеля

Write-Host "=== Тестирование Telegram бота локально ===" -ForegroundColor Green

# Проверка наличия ngrok
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue
if (-not $ngrokPath) {
    Write-Host "❌ ngrok не установлен. Скачайте с https://ngrok.com/download" -ForegroundColor Red
    Write-Host "Установка: choco install ngrok" -ForegroundColor Yellow
    exit 1
}

# Запуск Django сервера в фоне
Write-Host "🚀 Запуск Django сервера..." -ForegroundColor Blue
$djangoJob = Start-Job -ScriptBlock {
    cd "C:\Users\user\Desktop\GGame"
    python manage.py runserver 8000
}

Start-Sleep -Seconds 3

# Запуск ngrok туннеля
Write-Host "🌐 Запуск ngrok туннеля..." -ForegroundColor Blue
$ngrokJob = Start-Job -ScriptBlock {
    ngrok http 8000
}

Start-Sleep -Seconds 5

# Получение ngrok URL
Write-Host "🔗 Получение ngrok URL..." -ForegroundColor Blue
try {
    $ngrokApi = Invoke-RestMethod -Uri "http://localhost:4040/api/tunnels" -Method Get
    $tunnel = $ngrokApi.tunnels | Where-Object { $_.proto -eq "https" } | Select-Object -First 1
    $ngrokUrl = $tunnel.public_url

    Write-Host "✅ Ngrok URL: $ngrokUrl" -ForegroundColor Green

    # Установка webhook
    Write-Host "🔧 Установка webhook..." -ForegroundColor Blue
    $webhookUrl = "$ngrokUrl/api/telegram/webhook/"
    python manage.py set_webhook --url $webhookUrl

    Write-Host "" -ForegroundColor White
    Write-Host "🎯 Тестирование бота:" -ForegroundColor Cyan
    Write-Host "1. Найдите бота @MerzoitCodeBot в Telegram" -ForegroundColor White
    Write-Host "2. Напишите /start" -ForegroundColor White
    Write-Host "3. Нажмите кнопку '🎮 Начать игру'" -ForegroundColor White
    Write-Host "" -ForegroundColor White
    Write-Host "🛑 Для остановки нажмите Ctrl+C" -ForegroundColor Yellow

    # Ожидание остановки
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    }
    finally {
        Write-Host "🧹 Очистка..." -ForegroundColor Blue
        # Удаление webhook
        python manage.py delete_webhook
        # Остановка заданий
        Stop-Job $djangoJob -ErrorAction SilentlyContinue
        Stop-Job $ngrokJob -ErrorAction SilentlyContinue
        Remove-Job $djangoJob -ErrorAction SilentlyContinue
        Remove-Job $ngrokJob -ErrorAction SilentlyContinue
    }

} catch {
    Write-Host "❌ Ошибка получения ngrok URL: $_" -ForegroundColor Red
    Write-Host "Убедитесь, что ngrok запущен: ngrok http 8000" -ForegroundColor Yellow

    # Очистка
    Stop-Job $djangoJob -ErrorAction SilentlyContinue
    Remove-Job $djangoJob -ErrorAction SilentlyContinue
}
