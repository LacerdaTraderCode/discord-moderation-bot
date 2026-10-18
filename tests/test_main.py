"""Tests for the bot entry point."""

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock

import pytest
from discord.ext import commands

from bot import main as bot_main


@pytest.fixture
def bot(monkeypatch):
    """A bot whose extension loading, database setup and command sync are mocked."""
    monkeypatch.setattr(bot_main, "init_db", MagicMock())
    instance = bot_main.ModerationBot()
    instance.load_extension = AsyncMock()
    instance.tree.sync = AsyncMock(return_value=[])
    return instance


def test_setup_hook_initializes_the_database_and_loads_every_cog(bot):
    asyncio.run(bot.setup_hook())

    bot_main.init_db.assert_called_once_with()
    loaded = [call.args[0] for call in bot.load_extension.await_args_list]
    assert loaded == ["bot.cogs.moderation", "bot.cogs.utility", "bot.cogs.events"]
    bot.tree.sync.assert_awaited_once()


def test_a_cog_that_fails_to_load_does_not_stop_the_others(bot, caplog):
    def fake_load(name):
        if name.endswith("utility"):
            raise commands.ExtensionNotFound(name)

    bot.load_extension = AsyncMock(side_effect=fake_load)

    with caplog.at_level(logging.ERROR, logger="bot.main"):
        asyncio.run(bot.setup_hook())

    assert bot.load_extension.await_count == 3
    assert "Erro carregando utility" in caplog.text
    bot.tree.sync.assert_awaited_once()


def test_unexpected_errors_while_loading_are_not_swallowed(bot):
    bot.load_extension = AsyncMock(side_effect=RuntimeError("boom"))

    with pytest.raises(RuntimeError):
        asyncio.run(bot.setup_hook())


def test_the_command_prefix_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("COMMAND_PREFIX", "?")

    assert bot_main.ModerationBot().command_prefix == "?"


def test_the_default_command_prefix_is_an_exclamation_mark(monkeypatch):
    monkeypatch.delenv("COMMAND_PREFIX", raising=False)

    assert bot_main.ModerationBot().command_prefix == "!"


def test_the_bot_requests_the_message_content_and_members_intents():
    instance = bot_main.ModerationBot()

    assert instance.intents.message_content is True
    assert instance.intents.members is True


def test_main_requires_a_token(monkeypatch):
    monkeypatch.delenv("DISCORD_TOKEN", raising=False)

    with pytest.raises(ValueError, match="DISCORD_TOKEN"):
        asyncio.run(bot_main.main())


def test_main_starts_the_bot_with_the_configured_token(monkeypatch):
    fake_bot = MagicMock()
    fake_bot.start = AsyncMock()
    monkeypatch.setenv("DISCORD_TOKEN", "test-token")
    monkeypatch.setattr(bot_main, "ModerationBot", MagicMock(return_value=fake_bot))

    asyncio.run(bot_main.main())

    fake_bot.start.assert_awaited_once_with("test-token")
