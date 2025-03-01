# Sveltekit Static Github Page Template

Everything you need to setup a github static page using sveltekit and tailwindcss

## Prerequisites
- [Node](https://nodejs.org/en/download)
- [Just](https://github.com/casey/just)

## Setup Development
```bash
just setup [bun|npm|pnpm] # setup the project with the package manager of your choice
```

## Development
There are two main ways to develop this application, either on the web or using a android/ios device. So far, we're only going to focus on an android device. 

### Web Development
If you want to develop on the web (if you for some reason can't use AndroidStudio), just running the command
```bash
just // Or [bun|npm|pnpm] run dev
```
is enough to start a web development session. Although, you might want to turn on responsive design mode ( or hit `Ctrl+Shift+M` ). In my experience, IPhone 11 works properly enough.

### Device Development
By running the command
```bash
just android
```
you'll be running the following commands:
```bash
bun run build // Builds the project
npx cap sync // Syncs the built files to android and ios
npx cap open android // Opens android studio to this project
```
And then from within android studio, hit the play button. Whenever you re-run just android, you'll also have to restart the app on android studio. The good thing with this is that you can easily connect a physical device, like an actual phone to test everything.


## Git Management

### Pushing your changes
While we should have strict guidelines on how to push your changes (like having every new feature in its own branch which will be merged with the main branch), You can start off with the scripts i've designated in the `justfile`

#### Pushing without CI/CD
```bash
just push "<your-commit-message>"
```
This command runs the following commands:
```bash
git add .
git commit -m "<your-commit-message>"
git push
```
I recommend only using just after you've already gotten accustomed to the git cli.

#### Pushing with CI/CD
As of now, there are no github actions that automatically build and package the application into an apk and whatever ios has. But there will be. for now, i've setup a placeholder command for this specific purpose
```bash
just release "<your-commit-message>"
```
This is basically identical to the `just push` command with one minor change, the git message is pre-pended with "[release]". This is what this script runs:
```bash
git add .
git commit -m "[release] <your-commit-message>"
git push
```