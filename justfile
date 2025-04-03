
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

# Starts the web version of the app
[working-directory: './app']
web:
    bun run dev

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


# Set up node-red for api testing
api-test:
    docker rm -f eday-nodered 
    docker run -it -p 1880:1880 -v eday-nodered:/data --name eday-nodered nodered/node-red

# Compose the whole project or a specific set of services
[working-directory: './']
dc SERVICE="":
    docker compose up -d --build {{SERVICE}}

# Stops the docker compose
[working-directory: './']
dc-down SERVICE="":
    docker compose down {{SERVICE}}

# Compose only a specific service using a alternative file
[working-directory: './']
dc-alt ALT SERVICE="":
    docker compose -f docker-compose.yml -f docker-compose-{{ALT}}.yml up -d --build {{SERVICE}}

# Builds a specific service with an alt file while also sh into it.
[working-directory: './']
dc-int ALT SERVICE="":
    just dc-spec-alt {{ALT}} {{SERVICE}} 
    docker exec -it {{SERVICE}} sh
