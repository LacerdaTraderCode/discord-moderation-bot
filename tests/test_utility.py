"""Tests for the utility commands."""

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from bot.cogs.utility import Utility


def make_interaction():
    interaction = MagicMock()
    interaction.response.send_message = AsyncMock()
    return interaction


def make_member(name="Alice"):
    member = MagicMock()
    member.display_name = name
    member.display_avatar.url = "https://example.com/avatar.png"
    member.display_avatar.with_size.return_value.url = "https://example.com/big.png"
    return member


def make_user(joined_at=None, roles=None):
    member = make_member()
    member.name = "alice"
    member.id = 2
    member.bot = False
    member.color = discord.Color(0)
    member.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
    member.joined_at = joined_at
    member.roles = roles or []
    return member


def call(command, *args, latency=0.05):
    bot = MagicMock()
    bot.latency = latency
    asyncio.run(command.callback(Utility(bot), *args))


def embed_of(interaction):
    return interaction.response.send_message.await_args.kwargs["embed"]


@pytest.mark.parametrize(
    ("latency", "emoji", "milliseconds"),
    [(0.05, "🟢", 50), (0.2, "🟡", 200), (0.5, "🔴", 500)],
)
def test_ping_reports_the_latency_with_a_status_emoji(latency, emoji, milliseconds):
    interaction = make_interaction()

    call(Utility.ping, interaction, latency=latency)

    text = interaction.response.send_message.await_args.args[0]
    assert emoji in text
    assert f"{milliseconds}ms" in text


def test_avatar_shows_the_large_version():
    interaction, member = make_interaction(), make_member()

    call(Utility.avatar, interaction, member)

    embed = embed_of(interaction)
    assert "Alice" in embed.title
    assert embed.image.url == "https://example.com/big.png"
    member.display_avatar.with_size.assert_called_once_with(1024)


def test_avatar_defaults_to_the_command_author():
    interaction = make_interaction()
    interaction.user = make_member("Bob")

    call(Utility.avatar, interaction, None)

    assert "Bob" in embed_of(interaction).title


def test_userinfo_describes_the_member():
    role = MagicMock()
    role.mention = "<@&5>"
    member = make_user(
        joined_at=datetime(2021, 6, 1, tzinfo=timezone.utc),
        roles=[MagicMock(), role],
    )
    interaction = make_interaction()

    call(Utility.userinfo, interaction, member)

    embed = embed_of(interaction)
    fields = {field.name: field.value for field in embed.fields}
    assert "Alice" in embed.title
    assert fields["Nome de usuário"] == "`alice`"
    assert fields["ID"] == "`2`"
    assert fields["Bot?"] == "Não"
    assert "Entrou no servidor em" in fields
    assert fields["Cargos (1)"] == "<@&5>"


def test_userinfo_without_join_date_or_roles():
    interaction = make_interaction()

    call(Utility.userinfo, interaction, make_user())

    names = [field.name for field in embed_of(interaction).fields]
    assert "Entrou no servidor em" not in names
    assert not any(name.startswith("Cargos") for name in names)


def test_userinfo_defaults_to_the_command_author():
    interaction = make_interaction()
    interaction.user = make_user()

    call(Utility.userinfo, interaction, None)

    assert "Alice" in embed_of(interaction).title


def test_serverinfo_summarizes_the_server():
    interaction = make_interaction()
    guild = interaction.guild
    guild.name = "Test Guild"
    guild.description = None
    guild.icon = None
    guild.id = 1
    guild.owner = None
    guild.created_at = datetime(2019, 5, 5, tzinfo=timezone.utc)
    guild.member_count = 10
    guild.channels = [1, 2, 3]
    guild.roles = [1, 2]
    guild.premium_tier = 1
    guild.premium_subscription_count = 4
    guild.emojis = []

    call(Utility.serverinfo, interaction)

    embed = embed_of(interaction)
    values = [field.value for field in embed.fields]
    assert "Test Guild" in embed.title
    assert embed.description == "Sem descrição"
    assert "N/A" in values
    assert values[3:6] == ["10", "3", "2"]
