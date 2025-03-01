
default:
    bun run dev

# Builds project
build:
    bun run build

# Builds the project and syncs with android and ios
sync:
    bun run build
    npx cap sync


# Runs 'just sync' and then opens android studio
android:
    just sync
    npx cap open android

# Initialize this project with a package manager
setup PACKAGE_MANAGER='bun':
    {{PACKAGE_MANAGER}} i

# Run something, im not sure what
stack NAME='testing':
    echo "Running Stack Command! {{NAME}}"

# Push your project with the release flag
release MESSAGE:
    git add .
    git commit -m "[release] {{MESSAGE}}"
    git push

# Push your project normally
push MESSAGE:
    git add .
    git commit -m "{{MESSAGE}}"
    git push
