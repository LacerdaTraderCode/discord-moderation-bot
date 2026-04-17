"""
Cog Utility - comandos utilitários (ping, userinfo, serverinfo, avatar).
"""
import discord
from discord import app_commands
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Mostra a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        emoji = "🟢" if latency < 100 else "🟡" if latency < 300 else "🔴"
        await interaction.response.send_message(
            f"{emoji} Pong! Latência: **{latency}ms**"
        )

    @app_commands.command(name="userinfo", description="Informações sobre um usuário")
    @app_commands.describe(member="Usuário (padrão: você)")
    async def userinfo(
        self, interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user

        embed = discord.Embed(
            title=f"👤 {member.display_name}",
            color=member.color if member.color.value else discord.Color.blue(),
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Nome de usuário", value=f"`{member.name}`", inline=True)
        embed.add_field(name="ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name="Bot?", value="Sim" if member.bot else "Não", inline=True)

        embed.add_field(
            name="Conta criada em",
            value=f"<t:{int(member.created_at.timestamp())}:D>",
            inline=True,
        )
        if member.joined_at:
            embed.add_field(
                name="Entrou no servidor em",
                value=f"<t:{int(member.joined_at.timestamp())}:D>",
                inline=True,
            )

        roles = [r.mention for r in member.roles[1:]]  # remove @everyone
        if roles:
            embed.add_field(
                name=f"Cargos ({len(roles)})",
                value=", ".join(roles[:10]) + ("..." if len(roles) > 10 else ""),
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverinfo", description="Informações sobre o servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild

        embed = discord.Embed(
            title=f"📊 {g.name}",
            description=g.description or "Sem descrição",
            color=discord.Color.blue(),
        )
        if g.icon:
            embed.set_thumbnail(url=g.icon.url)

        embed.add_field(name="ID", value=f"`{g.id}`", inline=True)
        embed.add_field(name="Dono", value=g.owner.mention if g.owner else "N/A", inline=True)
        embed.add_field(
            name="Criado em",
            value=f"<t:{int(g.created_at.timestamp())}:D>",
            inline=True,
        )

        embed.add_field(name="👥 Membros", value=str(g.member_count), inline=True)
        embed.add_field(name="💬 Canais", value=str(len(g.channels)), inline=True)
        embed.add_field(name="🎭 Cargos", value=str(len(g.roles)), inline=True)

        embed.add_field(name="🚀 Boost Level", value=str(g.premium_tier), inline=True)
        embed.add_field(name="⚡ Boosts", value=str(g.premium_subscription_count), inline=True)
        embed.add_field(name="😀 Emojis", value=str(len(g.emojis)), inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="Mostra o avatar em alta resolução")
    @app_commands.describe(member="Usuário (padrão: você)")
    async def avatar(
        self, interaction: discord.Interaction,
        member: discord.Member = None
    ):
        member = member or interaction.user
        embed = discord.Embed(
            title=f"🖼️ Avatar de {member.display_name}",
            color=discord.Color.blue(),
        )
        embed.set_image(url=member.display_avatar.with_size(1024).url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Utility(bot))
