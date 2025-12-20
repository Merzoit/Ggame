# Скрипт для создания админа на Railway

$RAILWAY_URL = "https://web-production-051b.up.railway.app"
$SETUP_KEY = "ggame_setup_2025"

Write-Host "👤 Создание суперпользователя на Railway..." -ForegroundColor Green
Write-Host "URL: $RAILWAY_URL" -ForegroundColor Blue
Write-Host ""

Write-Host "🔑 Отправка запроса на создание админа..." -ForegroundColor Yellow

try {
    $url = "$RAILWAY_URL/api/telegram/create_admin/?key=$SETUP_KEY"
    $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 30

    if ($response.StatusCode -eq 200) {
        $data = $response.Content | ConvertFrom-Json

        Write-Host ""
        Write-Host "🎉 Результат:" -ForegroundColor Green

        if ($data.status -eq 'success') {
            Write-Host "   [SUCCESS] Админ создан!" -ForegroundColor Green
            Write-Host "   Логин: $($data.login)" -ForegroundColor Cyan
            Write-Host "   Пароль: $($data.password)" -ForegroundColor Cyan
            Write-Host "   URL: $($data.admin_url)" -ForegroundColor Cyan
        } elseif ($data.status -eq 'warning') {
            Write-Host "   [WARNING] Админ уже существует" -ForegroundColor Yellow
            Write-Host "   Логин: $($data.login)" -ForegroundColor Cyan
            Write-Host "   Пароль: $($data.password)" -ForegroundColor Cyan
            Write-Host "   URL: $($data.admin_url)" -ForegroundColor Cyan
        } else {
            Write-Host "   [ERROR] $($data.message)" -ForegroundColor Red
        }
    } else {
        Write-Host "   [ERROR] HTTP $($response.StatusCode)" -ForegroundColor Red
    }

} catch {
    Write-Host "   [ERROR] $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Возможные причины:" -ForegroundColor Yellow
    Write-Host "   • Railway еще передеплоится (подождите 2-3 минуты)" -ForegroundColor White
    Write-Host "   • Проверьте переменные окружения в Railway" -ForegroundColor White
    Write-Host "   • Проверьте логи Railway на ошибки" -ForegroundColor White
}

Write-Host ""
Write-Host "🔒 После создания админа этот эндпоинт будет недоступен!" -ForegroundColor Yellow
Write-Host "   Рекомендуется удалить маршрут create_admin из urls.py" -ForegroundColor Yellow
