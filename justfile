
[working-directory: './app']
default:
    bun run dev

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
