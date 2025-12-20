# 🚀 Быстрый деплой прямо сейчас

## Шаг 1: Railway (Django бэкенд)

1. **Перейдите на** https://railway.app
2. **Войдите через GitHub**
3. **Нажмите "New Project"**
4. **Выберите "Deploy from GitHub repo"**
5. **Найдите и выберите** `Merzoit/Ggame`
6. **Railway автоматически начнет деплой**
7. **Добавьте PostgreSQL:**
   - Нажмите "+" → "Database" → "PostgreSQL"
   - Выберите Free план
8. **Настройте переменные окружения:**
   ```
   SECRET_KEY=c6r(6itgmz&4cx2(s=e+xr91oh(oj94-!h_nb(%v&n_s%o^-7e
   DEBUG=False
   TELEGRAM_BOT_TOKEN=8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k
   FRONTEND_URL=https://ggame.vercel.app
   ```
9. **Получите URL бэкенда** (например: `https://ggame-production.up.railway.app`)
10. **Обновите TELEGRAM_WEBHOOK_URL:**
    ```
    TELEGRAM_WEBHOOK_URL=https://ggame-production.up.railway.app
    ```

## Шаг 2: Vercel (Vue.js фронтенд)

1. **Перейдите на** https://vercel.com
2. **Войдите через GitHub**
3. **Нажмите "Add New" → "Project"**
4. **Выберите репозиторий** `Merzoit/Ggame`
5. **Настройте папку:**
   - **Root Directory:** `frontend-vue`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. **Добавьте переменную окружения:**
   ```
   VITE_API_BASE_URL=https://ВАШ_RAILWAY_URL/api
   ```
7. **Нажмите "Deploy"**
8. **Получите URL фронтенда** (например: `https://ggame.vercel.app`)

## Шаг 3: Финальная настройка

1. **Обновите FRONTEND_URL в Railway:**
   ```
   FRONTEND_URL=https://ВАШ_VERCEL_URL
   ```

2. **Перезапустите Railway сервис**

3. **Протестируйте:**
   - Напишите `/start` боту @MerzoitCodeBot
   - Нажмите "🎮 Начать игру"
   - Должно открыться веб-приложение

## ⚙️ Переменные окружения (полный список)

### Railway (бэкенд):
```
SECRET_KEY=c6r(6itgmz&4cx2(s=e+xr91oh(oj94-!h_nb(%v&n_s%o^-7e
DEBUG=False
ALLOWED_HOSTS=ВАШ_RAILWAY_URL (без https://)
DATABASE_URL=автоматически_из_PostgreSQL
TELEGRAM_BOT_TOKEN=8567389465:AAGf6VKykyl6REaiDz-Vqu2QTacQbvURS7k
TELEGRAM_WEBHOOK_URL=https://ВАШ_RAILWAY_URL
FRONTEND_URL=https://ВАШ_VERCEL_URL
CORS_ALLOWED_ORIGINS=https://ВАШ_VERCEL_URL
```

### Vercel (фронтенд):
```
VITE_API_BASE_URL=https://ВАШ_RAILWAY_URL/api
```

## 🔍 Проверка статуса

После деплоя проверьте логи в Railway:
- Бот должен автоматически настроиться
- Должны примениться миграции
- Сервер должен запуститься

## 🎯 Готово!

Ваш Telegram бот @MerzoitCodeBot и веб-приложение будут работать онлайн!

**Время деплоя:** 10-15 минут
**Стоимость:** Бесплатно
