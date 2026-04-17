# 🤖 Discord Moderation Bot

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Bot de moderação para servidores Discord com comandos modernos **slash commands**, sistema de warns persistente em SQLite, filtros de spam e comandos utilitários. Construído com `discord.py` e arquitetura assíncrona.

---

## 📋 Funcionalidades

### 🛡️ Moderação
- ✅ `/kick` — Expulsa membro
- ✅ `/ban` — Bane membro
- ✅ `/warn` — Aplica advertência (persistente)
- ✅ `/warnings` — Lista advertências de um usuário
- ✅ `/clear` — Limpa mensagens em massa
- ✅ `/mute` — Silencia temporariamente

### 🔧 Utilitários
- ✅ `/ping` — Latência do bot
- ✅ `/userinfo` — Informações de um usuário
- ✅ `/serverinfo` — Informações do servidor
- ✅ `/avatar` — Mostra avatar em alta resolução

### 🎯 Automação
- ✅ Auto-detecção de spam (mensagens repetidas)
- ✅ Log automático em canal configurado
- ✅ Mensagem de boas-vindas para novos membros

---

## 🛠️ Tecnologias

- **discord.py 2.x** — Framework oficial
- **SQLAlchemy** — Persistência de warns
- **asyncio** — Assíncrono nativo
- **python-dotenv** — Configurações

---

## 📁 Estrutura

```
discord-moderation-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada
│   ├── database.py          # Persistência de warns
│   └── cogs/
│       ├── moderation.py    # Comandos de moderação
│       ├── utility.py       # Comandos utilitários
│       └── events.py        # Handlers de eventos
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação

### 1. Criar bot no Discord

1. Acesse [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação → Bot → copie o **Token**
3. Em "OAuth2 > URL Generator":
   - Scopes: `bot`, `applications.commands`
   - Permissions: `Administrator` (ou específicas)
4. Use a URL gerada para adicionar o bot ao seu servidor

### 2. Rodar localmente

```bash
git clone https://github.com/LacerdaTraderCode/discord-moderation-bot.git
cd discord-moderation-bot

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edite .env com seu DISCORD_TOKEN

python -m bot.main
```

---

## 💬 Uso

Após o bot estar online no servidor, digite `/` em qualquer canal para ver os comandos disponíveis.

### Exemplos

```
/warn @usuario Ofensa ao servidor
→ ⚠️ @usuario advertido. Motivo: Ofensa ao servidor (warn #1)

/warnings @usuario
→ @usuario possui 1 advertência:
  #1 - Ofensa ao servidor (há 2 minutos)

/clear 50
→ 🗑️ 50 mensagens removidas.

/userinfo @usuario
→ [embed com avatar, data de ingresso, roles, etc.]
```

---

## 🔐 Permissões Necessárias

O bot precisa destas permissões no servidor:
- Ler mensagens
- Enviar mensagens
- Gerenciar mensagens (para `/clear`)
- Expulsar membros (para `/kick`)
- Banir membros (para `/ban`)
- Moderar membros (para `/mute`)

---

## 🚀 Deploy 24/7

- **Railway** ou **Render** (planos free)
- **Raspberry Pi** (ideal para uso pessoal)
- **VPS** (DigitalOcean, Contabo, Linode)

---

## 👨‍💻 Autor

**Wagner Lacerda**  
🔗 [LinkedIn](https://www.linkedin.com/in/wagner-lacerda-da-silva-958b9481)  
🐙 [GitHub](https://github.com/LacerdaTraderCode)  

---

## 📄 Licença

MIT License
