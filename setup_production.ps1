# Скрипт настройки продакшена для Railway

Write-Host "🚀 Настройка продакшена для GGame..." -ForegroundColor Green
Write-Host ""

# 1. Создание суперпользователя
Write-Host "1️⃣ Создание суперпользователя..." -ForegroundColor Yellow
try {
    python manage.py create_admin --username admin --email admin@ggame.com --password admin123
} catch {
    Write-Host "❌ Ошибка создания админа: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 2. Сборка статических файлов
Write-Host "2️⃣ Сборка статических файлов..." -ForegroundColor Yellow
try {
    python manage.py collectstatic --noinput --clear
    Write-Host "✅ Статические файлы собраны" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка сборки статических файлов: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# 3. Проверка миграций
Write-Host "3️⃣ Проверка миграций..." -ForegroundColor Yellow
try {
    python manage.py migrate --check
    Write-Host "✅ Миграции в порядке" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Есть непримененные миграции. Запустите: python manage.py migrate" -ForegroundColor Yellow
}

Write-Host ""

# 4. Настройка бота (если переменные установлены)
Write-Host "4️⃣ Настройка Telegram бота..." -ForegroundColor Yellow
try {
    python manage.py setup_bot
} catch {
    Write-Host "⚠️  Бот не настроен (возможно, переменные не установлены)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Настройка завершена!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Следующие шаги:" -ForegroundColor Cyan
Write-Host "  1. Задеплойте код на Railway" -ForegroundColor White
Write-Host "  2. Установите переменные окружения в Railway Dashboard" -ForegroundColor White
Write-Host "  3. Перейдите в админку: https://ВАШ_RAILWAY_URL/admin/" -ForegroundColor White
Write-Host "  4. Логин: admin, Пароль: admin123" -ForegroundColor White
Write-Host ""
Write-Host "🔗 Полезные ссылки:" -ForegroundColor Cyan
Write-Host "  Railway Dashboard: https://railway.app" -ForegroundColor White
Write-Host "  Админка: https://ВАШ_RAILWAY_URL/admin/" -ForegroundColor White
Write-Host "  Vercel Dashboard: https://vercel.com" -ForegroundColor White
