<div align="center">

# 🤖 Discord Moderation Bot

**Bot de moderação para servidores Discord com slash commands e warns persistentes**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-MIT-orange)](https://github.com/LacerdaTraderCode/discord-moderation-bot/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github)](https://github.com/LacerdaTraderCode/discord-moderation-bot)

</div>

---

## 📌 Sobre o projeto

Bot de moderação para servidores Discord com **slash commands** modernos, sistema de warns persistente em SQLite, filtros de spam e comandos utilitários. Construído com `discord.py 2.x` e arquitetura totalmente assíncrona.

### Funcionalidades

#### 🛡️ Moderação
- ✅ `/kick` — Expulsa membro
- ✅ `/ban` — Bane membro
- ✅ `/warn` — Aplica advertência (persistente em banco)
- ✅ `/warnings` — Lista advertências de um usuário
- ✅ `/clear` — Limpa mensagens em massa
- ✅ `/mute` — Silencia temporariamente

#### 🔧 Utilitários
- ✅ `/ping` — Latência do bot
- ✅ `/userinfo` — Informações detalhadas de um usuário
- ✅ `/serverinfo` — Estatísticas do servidor
- ✅ `/avatar` — Mostra avatar em alta resolução

#### 🎯 Automação
- ✅ Auto-detecção de spam (mensagens repetidas)
- ✅ Log automático em canal configurado
- ✅ Mensagem de boas-vindas para novos membros

---

## 🛠️ Tecnologias

- **discord.py 2.x** — Framework oficial com suporte a slash commands
- **SQLAlchemy** — Persistência de warns
- **asyncio** — Arquitetura assíncrona nativa
- **python-dotenv** — Configuração via variáveis de ambiente

---

## 📁 Estrutura

```
discord-moderation-bot/
├── bot/
│   ├── main.py              # Ponto de entrada
│   ├── database.py          # Persistência de warns
│   └── cogs/
│       ├── moderation.py    # Comandos de moderação
│       ├── utility.py       # Comandos utilitários
│       └── events.py        # Handlers de eventos
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📦 Instalação

### 1. Criar o bot no Discord Developer Portal

1. Acesse [discord.com/developers/applications](https://discord.com/developers/applications)
2. Crie nova aplicação → Bot → copie o **Token**
3. Em **OAuth2 > URL Generator**: scopes `bot` + `applications.commands`, permissão `Administrator`
4. Use a URL gerada para adicionar o bot ao servidor

### 2. Rodar localmente

```bash
git clone https://github.com/LacerdaTraderCode/discord-moderation-bot.git
cd discord-moderation-bot

python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

pip install -r requirements.txt

cp .env.example .env
# Edite .env e preencha DISCORD_TOKEN

python -m bot.main
```

---

## 💬 Exemplos de uso

```
/warn @usuario Ofensa ao servidor
→ ⚠️ @usuario advertido. Motivo: Ofensa ao servidor (warn #1)

/warnings @usuario
→ @usuario possui 1 advertência:
  #1 - Ofensa ao servidor (há 2 minutos)

/clear 50
→ 🗑️ 50 mensagens removidas.
```

---

## 🔐 Permissões necessárias

- Ler e enviar mensagens
- Gerenciar mensagens (para `/clear`)
- Expulsar e banir membros
- Moderar membros (para `/mute`)

---

## 🚀 Deploy 24/7

- **Railway** ou **Render** — planos gratuitos disponíveis
- **VPS** — DigitalOcean, Contabo, Linode
- **Raspberry Pi** — ideal para uso pessoal

---

## ✅ Requisitos

- Python **3.11** ou superior
- Token de bot do Discord

---

## 👤 Autor

<div align="center">

**Wagner Lacerda** — Python Backend Developer | APIs REST • Automação • Data Engineering

[![GitHub](https://img.shields.io/badge/GitHub-LacerdaTraderCode-181717?logo=github&logoColor=white)](https://github.com/LacerdaTraderCode)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wagner%20Lacerda-0077B5?logo=linkedin&logoColor=white)](https://linkedin.com/in/wagner-lacerda-da-silva-958b9481)
[![YouTube](https://img.shields.io/badge/YouTube-LacerdaTraderCode-FF0000?logo=youtube&logoColor=white)](https://youtube.com/@LacerdaTraderCode)
[![Telegram](https://img.shields.io/badge/Telegram-LacerdaTraderCode-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode)
[![Telegram Bots](https://img.shields.io/badge/Telegram-Bots-26A5E4?logo=telegram&logoColor=white)](https://t.me/LacerdaTraderCode_bots)

📍 Rio Grande do Sul, Brasil

</div>

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
