"""
Cog de Moderação - comandos de kick, ban, warn, clear, mute.
"""
import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

from bot.database import add_warning, get_warnings


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulsa um membro do servidor")
    @app_commands.describe(member="Membro a expulsar", reason="Motivo da expulsão")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self, interaction: discord.Interaction,
        member: discord.Member, reason: str = "Não especificado"
    ):
        try:
            await member.kick(reason=reason)
            await interaction.response.send_message(
                f"👢 {member.mention} foi expulso. Motivo: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Sem permissão para expulsar esse membro.", ephemeral=True
            )

    @app_commands.command(name="ban", description="Bane um membro do servidor")
    @app_commands.describe(member="Membro a banir", reason="Motivo do ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self, interaction: discord.Interaction,
        member: discord.Member, reason: str = "Não especificado"
    ):
        try:
            await member.ban(reason=reason, delete_message_days=1)
            await interaction.response.send_message(
                f"🔨 {member.mention} foi banido. Motivo: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Sem permissão para banir esse membro.", ephemeral=True
            )

    @app_commands.command(name="warn", description="Aplica uma advertência")
    @app_commands.describe(member="Membro a advertir", reason="Motivo")
    @app_commands.checks.has_permissions(kick_members=True)
    async def warn(
        self, interaction: discord.Interaction,
        member: discord.Member, reason: str
    ):
        w = add_warning(
            guild_id=interaction.guild.id,
            user_id=member.id,
            moderator_id=interaction.user.id,
            reason=reason,
        )
        count = len(get_warnings(interaction.guild.id, member.id))

        embed = discord.Embed(
            title="⚠️ Advertência Aplicada",
            color=discord.Color.orange(),
        )
        embed.add_field(name="Usuário", value=member.mention, inline=True)
        embed.add_field(name="Moderador", value=interaction.user.mention, inline=True)
        embed.add_field(name="Motivo", value=reason, inline=False)
        embed.set_footer(text=f"Warn #{w.id} · Total: {count}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="warnings", description="Lista advertências de um usuário")
    @app_commands.describe(member="Membro para consultar")
    async def warnings_cmd(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        warns = get_warnings(interaction.guild.id, member.id)

        if not warns:
            await interaction.response.send_message(
                f"✅ {member.mention} não tem advertências."
            )
            return

        embed = discord.Embed(
            title=f"⚠️ Advertências de {member.display_name}",
            description=f"Total: **{len(warns)}**",
            color=discord.Color.orange(),
        )
        for w in warns[:10]:
            embed.add_field(
                name=f"#{w.id} · <t:{int(w.created_at.timestamp())}:R>",
                value=w.reason,
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Remove N mensagens do canal")
    @app_commands.describe(amount="Quantidade (1-100)")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount < 1 or amount > 100:
            await interaction.response.send_message(
                "❌ Quantidade deve estar entre 1 e 100.", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(
            f"🗑️ {len(deleted)} mensagens removidas.", ephemeral=True
        )

    @app_commands.command(name="mute", description="Silencia membro por tempo determinado")
    @app_commands.describe(member="Membro", minutes="Minutos (1-1440)", reason="Motivo")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(
        self, interaction: discord.Interaction,
        member: discord.Member, minutes: int, reason: str = "Não especificado"
    ):
        if minutes < 1 or minutes > 1440:
            await interaction.response.send_message(
                "❌ Tempo deve estar entre 1 e 1440 minutos (24h).", ephemeral=True
            )
            return

        try:
            await member.timeout(timedelta(minutes=minutes), reason=reason)
            await interaction.response.send_message(
                f"🔇 {member.mention} silenciado por {minutes} min. Motivo: {reason}"
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ Sem permissão para silenciar esse membro.", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderation(bot))
