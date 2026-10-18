"""Tests for the warning persistence layer."""

from sqlalchemy import inspect

from bot.database import add_warning, get_warnings, init_db


def test_init_db_creates_the_warnings_table(engine):
    init_db()

    assert inspect(engine).has_table("warnings")


def test_add_warning_returns_the_stored_warning(db):
    warning = add_warning(guild_id=1, user_id=2, moderator_id=3, reason="spam")

    assert warning.id is not None
    assert (warning.guild_id, warning.user_id, warning.moderator_id) == (1, 2, 3)
    assert warning.reason == "spam"
    assert warning.created_at is not None


def test_get_warnings_returns_every_warning_of_the_user(db):
    add_warning(1, 2, 9, "spam")
    add_warning(1, 2, 9, "flood")

    reasons = sorted(warning.reason for warning in get_warnings(1, 2))

    assert reasons == ["flood", "spam"]


def test_get_warnings_filters_by_guild_and_user(db):
    add_warning(1, 2, 9, "mine")
    add_warning(1, 3, 9, "other user")
    add_warning(7, 2, 9, "other guild")

    reasons = [warning.reason for warning in get_warnings(1, 2)]

    assert reasons == ["mine"]


def test_get_warnings_is_empty_for_a_user_without_warnings(db):
    assert get_warnings(1, 2) == []
