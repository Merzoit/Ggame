# ⚡ Быстрый деплой GGame (5 минут)

## 🎯 Рекомендуемый вариант: Railway + Vercel

### Шаг 1: Django на Railway (2 минуты)

1. Откройте https://railway.app и войдите через GitHub
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите репозиторий `Merzoit/Ggame`
4. Добавьте PostgreSQL: "+ New" → "Database" → "PostgreSQL"
5. В "Variables" добавьте:
   ```
   SECRET_KEY=сгенерируйте-через-python-generate_secret_key.py
   DEBUG=False
   ```
6. Railway автоматически задеплоит! Получите URL (например: `https://ggame-production.up.railway.app`)

### Шаг 2: Vue на Vercel (2 минуты)

1. Откройте https://vercel.com и войдите через GitHub
2. Нажмите "Add New" → "Project"
3. Выберите репозиторий `Merzoit/Ggame`
4. **Важно:** Укажите:
   - Root Directory: `frontend-vue`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. В "Environment Variables" добавьте:
   ```
   VITE_API_BASE_URL=https://ваш-railway-url.railway.app/api
   ```
6. Нажмите "Deploy" - готово!

### Шаг 3: Обновите CORS (1 минута)

В Railway добавьте переменную:
```
CORS_ALLOWED_ORIGINS=https://ваш-vercel-url.vercel.app
```

Перезапустите сервис в Railway.

---

## ✅ Готово!

Теперь у вас есть:
- 🌐 Бэкенд: `https://ggame-production.up.railway.app`
- 🎨 Фронтенд: `https://ggame.vercel.app`

**Подробная инструкция:** См. [DEPLOY.md](DEPLOY.md)
