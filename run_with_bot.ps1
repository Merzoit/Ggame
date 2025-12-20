# Скрипт для запуска Django сервера с автоматической настройкой Telegram бота

param(
    [string]$Port = "8000",
    [switch]$NoBrowser,
    [switch]$Help
)

if ($Help) {
    Write-Host "Скрипт для запуска Django сервера с Telegram ботом" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Параметры:" -ForegroundColor Yellow
    Write-Host "  -Port <порт>      Порт для запуска сервера (по умолчанию: 8000)"
    Write-Host "  -NoBrowser        Не открывать браузер автоматически"
    Write-Host "  -Help             Показать эту справку"
    Write-Host ""
    Write-Host "Примеры использования:" -ForegroundColor Green
    Write-Host "  .\run_with_bot.ps1"
    Write-Host "  .\run_with_bot.ps1 -Port 3000"
    Write-Host "  .\run_with_bot.ps1 -NoBrowser"
    exit 0
}

Write-Host "🚀 Запуск GGame сервера с Telegram ботом..." -ForegroundColor Green
Write-Host ""

# Переходим в директорию проекта
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
cd $projectPath

# Проверяем наличие Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "🐍 $pythonVersion" -ForegroundColor Blue
} catch {
    Write-Host "❌ Python не найден. Установите Python и добавьте в PATH" -ForegroundColor Red
    exit 1
}

# Проверяем наличие виртуального окружения
$venvPath = "venv\Scripts\activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "🔧 Активация виртуального окружения..." -ForegroundColor Blue
    & $venvPath
} else {
    Write-Host "⚠️  Виртуальное окружение не найдено. Запуск без него..." -ForegroundColor Yellow
}

# Проверяем настройки Django
Write-Host "🔍 Проверка Django настроек..." -ForegroundColor Blue
try {
    python manage.py check --quiet
    Write-Host "✅ Django настройки корректны" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка в Django настройках: $_" -ForegroundColor Red
    exit 1
}

# Применяем миграции
Write-Host "🗃️  Применение миграций..." -ForegroundColor Blue
try {
    python manage.py migrate --verbosity 0
    Write-Host "✅ Миграции применены" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка применения миграций: $_" -ForegroundColor Red
    exit 1
}

# Настраиваем Telegram бота
Write-Host "🤖 Настройка Telegram бота..." -ForegroundColor Blue
try {
    $botSetup = python manage.py setup_bot --force 2>&1
    if ($botSetup -match "успешно настроен") {
        Write-Host "✅ Telegram бот настроен" -ForegroundColor Green
        # Выводим только важную информацию
        $botSetup | Where-Object { $_ -match "Бот найден|@|URL|успешно" } | ForEach-Object {
            Write-Host "   $_" -ForegroundColor Gray
        }
    } else {
        Write-Host "⚠️  Проблемы с настройкой бота:" -ForegroundColor Yellow
        Write-Host $botSetup -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Ошибка настройки бота: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🌐 Запуск Django сервера на порту $Port..." -ForegroundColor Green
Write-Host "📱 Доступно по адресу: http://localhost:$Port" -ForegroundColor Cyan
Write-Host "🤖 Бот будет автоматически настроен при запуске сервера" -ForegroundColor Cyan
Write-Host ""

# Открываем браузер (если не отключено)
if (-not $NoBrowser) {
    Start-Job -ScriptBlock {
        Start-Sleep -Seconds 3
        Start-Process "http://localhost:$using:Port"
    } | Out-Null
}

# Запускаем сервер
try {
    python manage.py runserver "0.0.0.0:$Port"
} catch {
    Write-Host "❌ Ошибка запуска сервера: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "🛑 Сервер остановлен" -ForegroundColor Yellow
}
