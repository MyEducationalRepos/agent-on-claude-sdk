"""Unit tests for the PostgreSQL metadata adapter stub."""

import pytest

from agent_on_claude_sdk.models import RunRecord
from agent_on_claude_sdk.persistence.pg_store import PgStore


@pytest.fixture()
def store() -> PgStore:
    return PgStore(dsn="postgresql://user:pass@localhost:5432/testdb")


class TestPgStoreInterface:
    def test_importable(self):
        from agent_on_claude_sdk.persistence.pg_store import PgStore  # noqa: F401

    def test_accepts_dsn(self):
        s = PgStore(dsn="postgresql://localhost/db")
        assert s._dsn == "postgresql://localhost/db"

    def test_save_raises_not_implemented(self, store: PgStore):
        r = RunRecord(task="t", model="m")
        with pytest.raises(NotImplementedError):
            store.save(r)

    def test_load_raises_not_implemented(self, store: PgStore):
        with pytest.raises(NotImplementedError):
            store.load("some-run-id")

    def test_list_runs_raises_not_implemented(self, store: PgStore):
        with pytest.raises(NotImplementedError):
            store.list_runs()
