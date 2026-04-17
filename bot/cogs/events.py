"""
Cog Events - handlers de eventos (welcome, anti-spam).
"""
import os
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Events(commands.Cog):
    """Handlers automatizados: boas-vindas e anti-spam básico."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Histórico de mensagens por usuário (para anti-spam)
        self.user_messages = defaultdict(lambda: deque(maxlen=5))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Envia mensagem de boas-vindas quando alguém entra."""
        # Procura canal chamado 'boas-vindas', 'welcome' ou 'geral'
        channel = None
        for name in ["boas-vindas", "welcome", "geral", "general"]:
            channel = discord.utils.get(member.guild.text_channels, name=name)
            if channel:
                break

        if not channel:
            return

        embed = discord.Embed(
            title=f"🎉 Bem-vindo(a), {member.display_name}!",
            description=(
                f"Olá {member.mention}, seja bem-vindo(a) ao **{member.guild.name}**!\n"
                "Leia as regras e aproveite a comunidade. 👋"
            ),
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Agora somos {member.guild.member_count} membros")

        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Detecta spam simples (mesma mensagem repetida rápido)."""
        # Ignora bots e DMs
        if message.author.bot or not message.guild:
            return

        key = (message.guild.id, message.author.id)
        now = datetime.now()

        # Adiciona mensagem atual ao histórico
        self.user_messages[key].append((now, message.content))

        # Conta quantas mensagens iguais nos últimos 10 segundos
        recent = [
            content for ts, content in self.user_messages[key]
            if now - ts < timedelta(seconds=10) and content == message.content
        ]

        # Se 3+ iguais, deleta e avisa
        if len(recent) >= 3:
            try:
                await message.delete()
                await message.channel.send(
                    f"⚠️ {message.author.mention}, evite spam!",
                    delete_after=5,
                )
                logger.info(f"Anti-spam: removida mensagem de {message.author}")
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Trata erros de comandos globalmente."""
        if isinstance(error, commands.CommandNotFound):
            return
        logger.error(f"Erro em comando: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
