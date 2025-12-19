# Скрипт настройки подключения к GitHub для проекта GGame

param(
    [string]$RepoUrl
)

$env:Path += ";C:\Program Files\Git\bin"
cd "C:\Users\user\Desktop\GGame"

if (-not $RepoUrl) {
    Write-Host "Укажите URL репозитория GitHub:"
    Write-Host "Пример: .\setup-github.ps1 -RepoUrl 'https://github.com/username/GGame.git'"
    Write-Host ""
    Write-Host "Или создайте новый репозиторий на GitHub:"
    Write-Host "1. Перейдите на https://github.com/new"
    Write-Host "2. Назовите репозиторий 'GGame'"
    Write-Host "3. Скопируйте URL и запустите скрипт с этим URL"
    exit 1
}

# Проверяем, не настроен ли уже remote origin
$existingRemote = git remote get-url origin 2>$null
if ($existingRemote) {
    Write-Host "Remote origin уже настроен: $existingRemote"
    Write-Host "Если нужно изменить, удалите текущий remote:"
    Write-Host "git remote remove origin"
    exit 1
}

# Добавляем remote origin
git remote add origin $RepoUrl
Write-Host "Добавлен remote origin: $RepoUrl"

# Проверяем SSH ключ
$sshKeyExists = Test-Path "$HOME/.ssh/id_ed25519.pub"
if ($sshKeyExists) {
    Write-Host ""
    Write-Host "SSH ключ найден. Добавьте этот публичный ключ в GitHub:"
    Write-Host "1. Скопируйте ключ ниже:"
    Write-Host "----------------------------------------"
    Get-Content "$HOME/.ssh/id_ed25519.pub"
    Write-Host "----------------------------------------"
    Write-Host "2. Перейдите в GitHub Settings > SSH and GPG keys"
    Write-Host "3. Нажмите 'New SSH key'"
    Write-Host "4. Вставьте ключ и сохраните"
    Write-Host ""

    # Пробуем подключиться к GitHub
    Write-Host "Проверяю подключение к GitHub..."
    $sshTest = & ssh -T git@github.com 2>&1
    if ($sshTest -match "successfully authenticated") {
        Write-Host "✓ SSH подключение работает!"
        # Отправляем код на GitHub
        & git push -u origin master
        Write-Host "✓ Код отправлен на GitHub!"
    } else {
        Write-Host "✗ SSH подключение не работает. Проверьте ключ в GitHub."
        Write-Host "Используйте HTTPS вместо SSH:"
        Write-Host "git remote set-url origin https://github.com/username/GGame.git"
    }
} else {
    Write-Host "SSH ключ не найден. Используйте Personal Access Token:"
    Write-Host "1. Создайте токен: GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)"
    Write-Host "2. Выберите scopes: repo, workflow"
    Write-Host "3. Скопируйте токен"
    Write-Host "4. Используйте URL с токеном: https://username:token@github.com/username/GGame.git"
}

Write-Host ""
Write-Host "Настройка завершена! Теперь можно использовать:"
Write-Host ".\git-workflow.ps1 -Action push  # Отправить изменения"
Write-Host ".\git-workflow.ps1 -Action pull  # Получить изменения"