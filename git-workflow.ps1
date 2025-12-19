# Скрипт для удобной работы с Git в проекте GGame

param(
    [string]$Action,
    [string]$Message,
    [string]$Branch
)

$env:Path += ";C:\Program Files\Git\bin"
cd "C:\Users\user\Desktop\GGame"

function Show-Help {
    Write-Host "Использование: .\git-workflow.ps1 -Action <действие> [параметры]"
    Write-Host ""
    Write-Host "Доступные действия:"
    Write-Host "  status     - Показать статус репозитория"
    Write-Host "  add        - Добавить все изменения (git add .)"
    Write-Host "  commit     - Зафиксировать изменения (нужен параметр -Message)"
    Write-Host "  push       - Отправить изменения на сервер"
    Write-Host "  pull       - Получить изменения с сервера"
    Write-Host "  branch     - Создать новую ветку (нужен параметр -Branch)"
    Write-Host "  checkout   - Перейти на ветку (нужен параметр -Branch)"
    Write-Host "  merge      - Слить ветку (нужен параметр -Branch)"
    Write-Host "  log        - Показать историю коммитов"
    Write-Host ""
    Write-Host "Примеры:"
    Write-Host "  .\git-workflow.ps1 -Action status"
    Write-Host "  .\git-workflow.ps1 -Action commit -Message 'Добавлена новая функция'"
    Write-Host "  .\git-workflow.ps1 -Action branch -Branch 'feature/new-feature'"
}

switch ($Action) {
    "status" {
        git status
    }
    "add" {
        git add .
        Write-Host "Все файлы добавлены в индекс"
    }
    "commit" {
        if ($Message) {
            git commit -m $Message
        } else {
            Write-Host "Ошибка: укажите сообщение коммита с параметром -Message"
        }
    }
    "push" {
        git push origin main
    }
    "pull" {
        git pull origin main
    }
    "branch" {
        if ($Branch) {
            git checkout -b $Branch
            Write-Host "Создана и переключена ветка: $Branch"
        } else {
            Write-Host "Ошибка: укажите имя ветки с параметром -Branch"
        }
    }
    "checkout" {
        if ($Branch) {
            git checkout $Branch
        } else {
            Write-Host "Ошибка: укажите имя ветки с параметром -Branch"
        }
    }
    "merge" {
        if ($Branch) {
            git merge $Branch
        } else {
            Write-Host "Ошибка: укажите имя ветки с параметром -Branch"
        }
    }
    "log" {
        git log --oneline -10
    }
    default {
        Show-Help
    }
}
