<div align="center">

# 🤖 Discord Moderation Bot

**A moderation bot for Discord servers with slash commands and persistent warnings**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-orange)](https://github.com/LacerdaTraderCode/discord-moderation-bot/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/discord-moderation-bot)

</div>

---

## 📌 About the Project

A moderation bot for Discord servers with modern **slash commands**, a persistent warning system backed by SQLite, spam filters, and utility commands. Built with `discord.py 2.x` on a fully asynchronous architecture.

### Features

#### 🛡️ Moderation
- ✅ `/kick` — Kicks a member
- ✅ `/ban` — Bans a member
- ✅ `/warn` — Issues a warning (persisted in the database)
- ✅ `/warnings` — Lists a user's warnings
- ✅ `/clear` — Bulk-clears messages
- ✅ `/mute` — Temporarily mutes a member

#### 🔧 Utilities
- ✅ `/ping` — Bot latency
- ✅ `/userinfo` — Detailed info about a user
- ✅ `/serverinfo` — Server statistics
- ✅ `/avatar` — Shows avatar in high resolution

#### 🎯 Automation
- ✅ Auto-detection of spam (repeated messages)
- ✅ Automatic logging to a configured channel
- ✅ Welcome message for new members

---

## 🛠️ Technologies

- **discord.py 2.x** — Official framework with slash command support
- **SQLAlchemy** — Warning persistence
- **asyncio** — Native asynchronous architecture
- **python-dotenv** — Configuration via environment variables

---

## 📁 Structure

```
discord-moderation-bot/
├── bot/
│   ├── main.py              # Entry point
│   ├── database.py          # Warning persistence
│   └── cogs/
│       ├── moderation.py    # Moderation commands
│       ├── utility.py       # Utility commands
│       └── events.py        # Event handlers
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📦 Installation

### 1. Create the bot on the Discord Developer Portal

1. Go to [discord.com/developers/applications](https://discord.com/developers/applications)
2. Create a new application → Bot → copy the **Token**
3. Under **OAuth2 > URL Generator**: scopes `bot` + `applications.commands`, permission `Administrator`
4. Use the generated URL to add the bot to your server

### 2. Run locally

```bash
git clone https://github.com/LacerdaTraderCode/discord-moderation-bot.git
cd discord-moderation-bot

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env and fill in DISCORD_TOKEN

python -m bot.main
```

---

## 💬 Usage Examples

```
/warn @user Server violation
→ ⚠️ @user warned. Reason: Server violation (warn #1)

/warnings @user
→ @user has 1 warning:
  #1 - Server violation (2 minutes ago)

/clear 50
→ 🗑️ 50 messages removed.
```

---

## 🔐 Required Permissions

- Read and send messages
- Manage messages (for `/clear`)
- Kick and ban members
- Moderate members (for `/mute`)

---

## 🚀 24/7 Deploy

- **Railway** or **Render** — free tiers available
- **VPS** — DigitalOcean, Contabo, Linode
- **Raspberry Pi** — ideal for personal use

---

## ✅ Requirements

- Python **3.11** or higher
- Discord bot token

---

## 👤 Author

<div align="center">

**Wagner Lacerda** — Senior Software Engineer | Python, Backend, AI Apps, Automation & Systems

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brazil

</div>

---

## 📄 License

Distributed under the MIT license. See [LICENSE](LICENSE) for more details.
