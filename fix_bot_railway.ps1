# Скрипт для исправления проблем с Telegram ботом на Railway

Write-Host "🔧 Исправление Telegram бота на Railway..." -ForegroundColor Green
Write-Host ""

# Шаг 1: Проверка локальных настроек
Write-Host "1️⃣ Проверка локальных настроек..." -ForegroundColor Blue
try {
    python manage.py check_deployment
} catch {
    Write-Host "❌ Ошибка проверки настроек: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2️⃣ Возможные проблемы и решения:" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔍 Проверьте в Railway Dashboard:" -ForegroundColor Yellow
Write-Host "   • Перейдите в ваш проект на https://railway.app" -ForegroundColor White
Write-Host "   • Выберите сервис GGame" -ForegroundColor White
Write-Host "   • Перейдите в раздел 'Variables'" -ForegroundColor White
Write-Host ""

Write-Host "⚙️  Убедитесь, что установлены переменные:" -ForegroundColor Yellow
Write-Host "   ✅ SECRET_KEY=c6r(6itgmz&4cx2(s=e+xr91oh(oj94-!h_nb(%v&n_s%o^-7e" -ForegroundColor Green
Write-Host "   ✅ DEBUG=False" -ForegroundColor Green
Write-Host "   ✅ TELEGRAM_BOT_TOKEN=8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k" -ForegroundColor Green
Write-Host "   ✅ TELEGRAM_WEBHOOK_URL=https://ВАШ-RAILWAY-URL" -ForegroundColor Green
Write-Host "   ✅ FRONTEND_URL=https://ВАШ-VERCEL-URL" -ForegroundColor Green
Write-Host "   ✅ CORS_ALLOWED_ORIGINS=https://ВАШ-VERCEL-URL" -ForegroundColor Green
Write-Host ""

Write-Host "🔄 Если переменные правильные, перезапустите сервис:" -ForegroundColor Yellow
Write-Host "   • В Railway нажмите 'Restart' на вашем сервисе" -ForegroundColor White
Write-Host ""

Write-Host "📝 Как найти URL'ы:" -ForegroundColor Yellow
Write-Host "   • Railway URL: в настройках сервиса (Settings > Domains)" -ForegroundColor White
Write-Host "   • Vercel URL: на главной странице проекта" -ForegroundColor White
Write-Host ""

Write-Host "🧪 Тестирование после исправления:" -ForegroundColor Cyan
Write-Host "   1. Напишите /start боту @MerzoitCodeBot" -ForegroundColor White
Write-Host "   2. Нажмите '🎮 Начать игру'" -ForegroundColor White
Write-Host "   3. Должно открыться веб-приложение" -ForegroundColor White
Write-Host ""

Write-Host "📞 Если проблема не решилась:" -ForegroundColor Red
Write-Host "   1. Проверьте логи Railway (Deployments > View Logs)" -ForegroundColor White
Write-Host "   2. Ищите сообщения об ошибках webhook" -ForegroundColor White
Write-Host "   3. Убедитесь, что домен Railway доступен из интернета" -ForegroundColor White
Write-Host ""

Write-Host "🎯 Готово! Следуйте инструкциям выше." -ForegroundColor Green
