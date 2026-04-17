"""
Discord Moderation Bot - Ponto de entrada.
"""
import os
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.database import init_db

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class ModerationBot(commands.Bot):
    """Bot principal - herda de commands.Bot para flexibilidade."""

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=os.getenv("COMMAND_PREFIX", "!"),
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        """Carrega cogs e sincroniza slash commands."""
        init_db()

        # Carregar cogs
        for cog in ["moderation", "utility", "events"]:
            try:
                await self.load_extension(f"bot.cogs.{cog}")
                logger.info(f"Cog carregado: {cog}")
            except Exception as e:
                logger.error(f"Erro carregando {cog}: {e}")

        # Sincronizar slash commands
        synced = await self.tree.sync()
        logger.info(f"Slash commands sincronizados: {len(synced)}")

    async def on_ready(self):
        logger.info(f"🤖 Bot online como {self.user} (ID: {self.user.id})")
        logger.info(f"📊 Servindo {len(self.guilds)} servidor(es)")
        await self.change_presence(
            activity=discord.Game(name="/help para comandos")
        )


async def main():
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN não configurado no .env")

    bot = ModerationBot()
    await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot encerrado.")
