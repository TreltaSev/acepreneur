# 🧠 AcePreneur

**AcePreneur** is the official app for the ACE Center's Entrepreneurship Day — a one-day event showcasing student-led programs, events, and innovations.

> 🚀 Built with SvelteKit + CapacitorJS on the frontend, and Python (Quart + MongoDB) on the backend.

---

## 📲 Features

- 🗓 **Events Page**  
  View live event info, announcements, and detailed pages for each activity.

- 🧑‍🍳 **Programs Directory**  
  Explore the wide variety of ACE Center programs like Culinary, Web Design, Event Planning, and more.

- 🗺 **Interactive Map**  
  See where events are happening in real-time with tappable pins and a QR-Powered “Find Me” feature.

- 🔍 **QR Code Scanner**  
  Scan codes to instantly open pages or gain temporary event admin privileges.

---

## 🛠 Tech Stack

| Layer         | Tech                         |
|---------------|------------------------------|
| Frontend      | SvelteKit + CapacitorJS      |
| Backend       | Python + Quart               |
| Database      | MongoDB                      |
| Auth / Access | One-day ID system, QR-based  |

---

## ⚙️ Dev Setup

```bash
# Clone the repo
git clone https://github.com/TreltaSev/acepreneur.git
cd acepreneur

# Install Tools
bun i -g rust-just

# Install dependencies (Frontend)
cd acepreneur/app
bun i

# Install dependencies (Backend)
# Installs Siblink (Required)
pip install git+https://github.com/TreltaSev/siblink.git

cd acepreneur/backend

siblink init

# Start the backend server
just backend

# Start the app in preview mode
just web
```
You also need a `.env.production.local` file for further configuration for keys like `MONGO_URL`

---

## 👷 Contribution Guide

### 🔀 Branch Naming
Use this format:

```php-template
feat/<feature-name>
fix/<bug-name>
chore/<misc>
```

Example PR title:
`Core: /events [List View]`

### 📝 Commit Messages
Follow this convention to keep history clean and readable:

```php-template
{type}({scope}): {short description}
```

If possible, you should add a description to the commit message.

Types you can use:
- `feat` – new feature
- `fix` – bug fix
- `chore` – non-functional change (docs, configs, etc)
- `refactor` – code improvements without changing functionality
- `style` – formatting, whitespace, etc
- `docs` – documentation changes


Thankfully it shouldn't be that hard to stick to these guidelines if you use the just commands
```bash
bash scripts/push.sh "feat(scope): Adding Things" "This is a very long description"
```

---


## 📦 Deployment

This app will be distributed through the Google Play Store and Apple App Store for Entrepreneurship Day only. After the event, the app may be deprecated or archived.

## 📚 License

MIT — feel free to fork and adapt this for your own school events, I wont mind :P