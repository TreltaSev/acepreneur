# Sveltekit Static Github Page Template

Everything you need to setup a github static page using sveltekit and tailwindcss

## Prerequisites
- [Node](https://nodejs.org/en/download)
- [Just](https://github.com/casey/just)

## Setup Development
```bash
just setup [bun|npm|pnpm] # setup the project with the package manager of your choice
```

## Release
```bash
just release "<release message>"
```
Adds all files, commits your message with git including the [release] flag, then pushes it. Initiating a release action on github.