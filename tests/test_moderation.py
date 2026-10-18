"""Tests for the moderation commands."""

import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock, MagicMock

import discord

from bot.cogs.moderation import Moderation
from bot.database import add_warning


def make_interaction():
    interaction = MagicMock()
    interaction.guild.id = 1
    interaction.user.id = 9
    interaction.user.mention = "<@9>"
    interaction.response.send_message = AsyncMock()
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()
    interaction.channel.purge = AsyncMock(return_value=[object(), object(), object()])
    return interaction


def make_member():
    member = MagicMock()
    member.id = 2
    member.mention = "<@2>"
    member.display_name = "Alice"
    member.kick = AsyncMock()
    member.ban = AsyncMock()
    member.timeout = AsyncMock()
    return member


def forbidden():
    return discord.Forbidden(MagicMock(status=403, reason="Forbidden"), "denied")


def call(command, *args):
    asyncio.run(command.callback(Moderation(MagicMock()), *args))


def reply(interaction):
    return interaction.response.send_message.await_args


def test_kick_removes_the_member_and_confirms():
    interaction, member = make_interaction(), make_member()

    call(Moderation.kick, interaction, member, "spam")

    member.kick.assert_awaited_once_with(reason="spam")
    text = reply(interaction).args[0]
    assert "<@2>" in text
    assert "spam" in text


def test_kick_uses_a_default_reason():
    interaction, member = make_interaction(), make_member()

    call(Moderation.kick, interaction, member)

    member.kick.assert_awaited_once_with(reason="Não especificado")


def test_kick_reports_missing_permissions():
    interaction, member = make_interaction(), make_member()
    member.kick = AsyncMock(side_effect=forbidden())

    call(Moderation.kick, interaction, member, "spam")

    assert reply(interaction).kwargs["ephemeral"] is True


def test_ban_removes_the_member_and_confirms():
    interaction, member = make_interaction(), make_member()

    call(Moderation.ban, interaction, member, "spam")

    member.ban.assert_awaited_once_with(reason="spam", delete_message_days=1)
    text = reply(interaction).args[0]
    assert "<@2>" in text
    assert "spam" in text


def test_ban_reports_missing_permissions():
    interaction, member = make_interaction(), make_member()
    member.ban = AsyncMock(side_effect=forbidden())

    call(Moderation.ban, interaction, member, "spam")

    assert reply(interaction).kwargs["ephemeral"] is True


def test_warn_stores_the_warning_and_reports_the_total(db):
    interaction, member = make_interaction(), make_member()

    call(Moderation.warn, interaction, member, "spam")
    call(Moderation.warn, interaction, member, "flood")

    stored = db.get_warnings(1, 2)
    assert sorted(warning.reason for warning in stored) == ["flood", "spam"]
    assert {warning.moderator_id for warning in stored} == {9}
    embed = reply(interaction).kwargs["embed"]
    assert "Total: 2" in embed.footer.text


def test_warnings_reports_a_clean_record(db):
    interaction, member = make_interaction(), make_member()

    call(Moderation.warnings_cmd, interaction, member)

    text = reply(interaction).args[0]
    assert "<@2>" in text
    assert "não tem advertências" in text


def test_warnings_lists_the_user_warnings(db):
    interaction, member = make_interaction(), make_member()
    add_warning(1, 2, 9, "spam")
    add_warning(1, 2, 9, "flood")

    call(Moderation.warnings_cmd, interaction, member)

    embed = reply(interaction).kwargs["embed"]
    assert "Alice" in embed.title
    assert "2" in embed.description
    assert sorted(field.value for field in embed.fields) == ["flood", "spam"]


def test_warnings_shows_at_most_ten_entries(db):
    interaction, member = make_interaction(), make_member()
    for number in range(12):
        add_warning(1, 2, 9, f"reason {number}")

    call(Moderation.warnings_cmd, interaction, member)

    embed = reply(interaction).kwargs["embed"]
    assert "12" in embed.description
    assert len(embed.fields) == 10


def test_clear_rejects_amounts_outside_the_limits():
    for amount in (0, 101):
        interaction = make_interaction()

        call(Moderation.clear, interaction, amount)

        assert reply(interaction).kwargs["ephemeral"] is True
        interaction.channel.purge.assert_not_awaited()


def test_clear_purges_the_requested_amount():
    interaction = make_interaction()

    call(Moderation.clear, interaction, 5)

    interaction.response.defer.assert_awaited_once_with(ephemeral=True)
    interaction.channel.purge.assert_awaited_once_with(limit=5)
    assert "3 mensagens" in interaction.followup.send.await_args.args[0]


def test_mute_rejects_durations_outside_the_limits():
    for minutes in (0, 1441):
        interaction, member = make_interaction(), make_member()

        call(Moderation.mute, interaction, member, minutes)

        assert reply(interaction).kwargs["ephemeral"] is True
        member.timeout.assert_not_awaited()


def test_mute_times_the_member_out():
    interaction, member = make_interaction(), make_member()

    call(Moderation.mute, interaction, member, 30, "spam")

    member.timeout.assert_awaited_once_with(timedelta(minutes=30), reason="spam")
    assert "30 min" in reply(interaction).args[0]


def test_mute_reports_missing_permissions():
    interaction, member = make_interaction(), make_member()
    member.timeout = AsyncMock(side_effect=forbidden())

    call(Moderation.mute, interaction, member, 30, "spam")

    assert reply(interaction).kwargs["ephemeral"] is True
