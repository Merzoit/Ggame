# 🚂 Настройка Railway для GGame

## 📋 Ваши URL:
- **Бэкенд (Railway):** https://web-production-051b.up.railway.app/
- **Фронтенд (Vercel):** https://ggame-psi.vercel.app/

## ⚙️ Настройка переменных окружения в Railway

Перейдите в **Railway Dashboard** → **Ваш проект GGame** → **Variables** и добавьте:

```
SECRET_KEY=c6r(6itgmz&4cx2(s=e+xr91oh(oj94-!h_nb(%v&n_s%o^-7e
DEBUG=False
ALLOWED_HOSTS=web-production-051b.up.railway.app
TELEGRAM_BOT_TOKEN=8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k
TELEGRAM_WEBHOOK_URL=https://web-production-051b.up.railway.app
FRONTEND_URL=https://ggame-psi.vercel.app
CORS_ALLOWED_ORIGINS=https://ggame-psi.vercel.app
```

## 🔄 После настройки переменных:

1. **Railway автоматически передеплоит** проект
2. **Бот автоматически настроится** с новыми URL
3. **Проверьте логи** в Railway (Deployments → View Logs)

## 🧪 Тестирование:

1. **Напишите `/start`** боту [@MerzoitCodeBot](https://t.me/MerzoitCodeBot)
2. **Нажмите "🎮 Начать игру"**
3. **Должно открыться:** https://ggame-psi.vercel.app/#/profile?user_id=ВАШ_TELEGRAM_ID

## 📊 Проверка работы:

### API тест:
```
https://web-production-051b.up.railway.app/api/telegram/test/
```

Должно вернуть: `{"status": "ok", "message": "Telegram webhook is working"}`

### Админка:
```
https://web-production-051b.up.railway.app/admin/
```
Логин: admin, Пароль: admin123

## 🔍 Диагностика:

Если что-то не работает, проверьте логи Railway и переменные окружения.

## ✅ Готово!

После настройки переменных ваш бот будет работать с реальными URL! 🚀
