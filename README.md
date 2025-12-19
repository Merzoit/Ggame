# GGame

Большой проект GGame.

## Установка и настройка

### Требования
- Python 3.x
- Git
- Windows PowerShell

### Первоначальная настройка проекта

1. **Git уже настроен!** Репозиторий инициализирован, базовые файлы созданы.

2. **Настройка GitHub подключения:**
   - Создайте новый репозиторий на GitHub (https://github.com/new)
   - Назовите его "GGame"
   - Запустите скрипт настройки:
   ```powershell
   .\setup-github.ps1 -RepoUrl "https://github.com/your-username/GGame.git"
   ```

3. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

### Клонирование существующего репозитория
```bash
git clone <repository-url>
cd GGame
```

## Разработка

### Запуск проекта
```bash
python main.py
```

### Работа с Git

#### Быстрый старт с PowerShell скриптом:

Для удобства создан PowerShell скрипт `git-workflow.ps1`. Запускать из папки проекта:

```powershell
# Проверить статус
.\git-workflow.ps1 -Action status

# Добавить и зафиксировать изменения
.\git-workflow.ps1 -Action add
.\git-workflow.ps1 -Action commit -Message "Описание изменений"

# Отправить/получить изменения
.\git-workflow.ps1 -Action push
.\git-workflow.ps1 -Action pull

# Работа с ветками
.\git-workflow.ps1 -Action branch -Branch "feature/new-feature"
.\git-workflow.ps1 -Action checkout -Branch "main"
.\git-workflow.ps1 -Action merge -Branch "feature/new-feature"

# Показать справку
.\git-workflow.ps1
```

#### Основные команды Git (альтернативный способ):
```bash
# Проверить статус
git status

# Добавить файлы
git add .

# Зафиксировать изменения
git commit -m "Описание изменений"

# Отправить на сервер
git push origin main

# Получить изменения с сервера
git pull origin main
```

#### Рабочий процесс:
1. Создайте новую ветку для каждой фичи: `git checkout -b feature/new-feature`
2. Внесите изменения
3. Зафиксируйте: `git commit -m "Описание"`
4. Перейдите на main: `git checkout main`
5. Обновите main: `git pull origin main`
6. Слейте ветку: `git merge feature/new-feature`
7. Отправьте изменения: `git push origin main`

## Структура проекта

```
GGame/
├── README.md
├── .gitignore
├── requirements.txt
└── src/
    └── main.py
```

## Авторы

- [Ваше имя]

## Лицензия

Этот проект лицензирован под MIT License.
