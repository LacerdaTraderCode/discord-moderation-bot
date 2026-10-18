"""Tests for the event handlers: anti-spam, welcome message and error logging."""

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock

import discord
from discord.ext import commands

from bot.cogs.events import Events


def make_cog():
    return Events(MagicMock())


def forbidden():
    return discord.Forbidden(MagicMock(status=403, reason="Forbidden"), "denied")


def make_message(content="hello", author_id=2, is_bot=False, in_guild=True):
    message = MagicMock()
    message.author.bot = is_bot
    message.author.id = author_id
    message.author.mention = f"<@{author_id}>"
    message.guild = MagicMock(id=1) if in_guild else None
    message.content = content
    message.delete = AsyncMock()
    message.channel.send = AsyncMock()
    return message


def receive(cog, message):
    asyncio.run(cog.on_message(message))


def make_member(channel_names):
    member = MagicMock()
    member.display_name = "Alice"
    member.mention = "<@2>"
    member.guild.name = "Test Guild"
    member.guild.member_count = 42
    member.display_avatar.url = "https://example.com/avatar.png"
    channels = []
    for name in channel_names:
        channel = MagicMock()
        channel.name = name
        channel.send = AsyncMock()
        channels.append(channel)
    member.guild.text_channels = channels
    return member, channels


def test_a_single_message_is_not_spam():
    cog = make_cog()
    message = make_message()

    receive(cog, message)

    message.delete.assert_not_awaited()


def test_the_third_identical_message_is_deleted_and_the_author_warned():
    cog = make_cog()
    messages = [make_message("buy now") for _ in range(3)]

    for message in messages:
        receive(cog, message)

    messages[0].delete.assert_not_awaited()
    messages[1].delete.assert_not_awaited()
    messages[2].delete.assert_awaited_once()
    warning = messages[2].channel.send.await_args
    assert "<@2>" in warning.args[0]
    assert warning.kwargs["delete_after"] == 5


def test_different_messages_are_not_spam():
    cog = make_cog()
    messages = [make_message(text) for text in ("one", "two", "three")]

    for message in messages:
        receive(cog, message)

    for message in messages:
        message.delete.assert_not_awaited()


def test_bots_and_direct_messages_are_ignored():
    cog = make_cog()
    ignored = [make_message("spam", is_bot=True) for _ in range(3)]
    ignored += [make_message("spam", in_guild=False) for _ in range(3)]

    for message in ignored:
        receive(cog, message)

    for message in ignored:
        message.delete.assert_not_awaited()
    assert not cog.user_messages


def test_spam_is_counted_per_user():
    cog = make_cog()
    messages = [
        make_message("spam", author_id=2),
        make_message("spam", author_id=2),
        make_message("spam", author_id=3),
    ]

    for message in messages:
        receive(cog, message)

    for message in messages:
        message.delete.assert_not_awaited()


def test_missing_permissions_do_not_break_the_anti_spam():
    cog = make_cog()
    messages = [make_message("spam") for _ in range(3)]
    messages[2].delete = AsyncMock(side_effect=forbidden())

    for message in messages:
        receive(cog, message)

    messages[2].delete.assert_awaited_once()
    messages[2].channel.send.assert_not_awaited()


def test_the_welcome_message_goes_to_the_welcome_channel():
    cog = make_cog()
    member, channels = make_member(["random", "welcome"])

    asyncio.run(cog.on_member_join(member))

    channels[0].send.assert_not_awaited()
    channels[1].send.assert_awaited_once()
    embed = channels[1].send.await_args.kwargs["embed"]
    assert "Alice" in embed.title
    assert "Test Guild" in embed.description
    assert "42" in embed.footer.text


def test_the_welcome_channel_names_have_a_priority_order():
    cog = make_cog()
    member, channels = make_member(["general", "welcome"])

    asyncio.run(cog.on_member_join(member))

    channels[0].send.assert_not_awaited()
    channels[1].send.assert_awaited_once()


def test_no_welcome_channel_means_no_message():
    cog = make_cog()
    member, channels = make_member(["random"])

    asyncio.run(cog.on_member_join(member))

    channels[0].send.assert_not_awaited()


def test_the_welcome_survives_missing_permissions():
    cog = make_cog()
    member, channels = make_member(["welcome"])
    channels[0].send = AsyncMock(side_effect=forbidden())

    asyncio.run(cog.on_member_join(member))

    channels[0].send.assert_awaited_once()


def test_unknown_commands_are_ignored(caplog):
    cog = make_cog()

    with caplog.at_level(logging.ERROR, logger="bot.cogs.events"):
        asyncio.run(cog.on_command_error(MagicMock(), commands.CommandNotFound()))

    assert "Erro em comando" not in caplog.text


def test_other_command_errors_are_logged(caplog):
    cog = make_cog()

    with caplog.at_level(logging.ERROR, logger="bot.cogs.events"):
        asyncio.run(cog.on_command_error(MagicMock(), commands.CommandError("boom")))

    assert "boom" in caplog.text
