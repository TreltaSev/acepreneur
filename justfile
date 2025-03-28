set shell := ["powershell.exe", "/c"]

[working-directory: './app']
default:
    bun run dev

# Runs the backend
[working-directory: './backend']
backend:
    just nginx-restart
    siblink run .


# Dumps and restarts nginx
[working-directory: './']
@nginx-restart:
    siblink run -- ./scripts/dev nginx dump
    siblink run -- ./scripts/dev nginx restart


# Runs the backend in a new console window
[working-directory: './']
backend-detached:
    Start-Process "cmd.exe" -ArgumentList "/c", "just nginx-restart"
    Start-Process "cmd.exe" -ArgumentList "/k", "just backend"

# Builds project
[working-directory: './app']
build:
    bun run build

# Builds the project and syncs with android and ios
[working-directory: './app']
sync:
    bun run build
    npx cap sync

# Runs 'just sync' and then opens android studio
[working-directory: './app']
android:
    just sync
    npx cap open android

# Initialize this project with a package manager
[working-directory: './app']
setup PACKAGE_MANAGER='bun':
    {{PACKAGE_MANAGER}} i

# Push your project with the release flag
[working-directory: './']
release MESSAGE:
    git add .
    git commit -m "[release] {{MESSAGE}}"
    git push

# Push your project normally
[working-directory: './']
push MESSAGE:
    git add .
    git commit -m "{{MESSAGE}}"
    git push
