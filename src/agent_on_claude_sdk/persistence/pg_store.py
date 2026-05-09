"""PostgreSQL metadata adapter stub.

This module reserves the architecture's optional metadata seam.
PostgreSQL is NOT required in Phase 1; all methods raise ``NotImplementedError``.
Replace this stub with a real SQLAlchemy/psycopg implementation when needed.
"""

from __future__ import annotations

from agent_on_claude_sdk.models import RunRecord


class PgStore:
    """Stub adapter matching the FsStore interface for optional PG metadata.

    Args:
        dsn: PostgreSQL Data Source Name, e.g.
            ``"postgresql://user:pass@localhost:5432/db"``.
            Stored but not used until the stub is replaced.
    """

    def __init__(self, dsn: str) -> None:
        self._dsn = dsn

    def save(self, record: RunRecord) -> None:  # noqa: ARG002
        raise NotImplementedError("PgStore is a stub; use FsStore for Phase 1.")

    def load(self, run_id: str) -> RunRecord:  # noqa: ARG002
        raise NotImplementedError("PgStore is a stub; use FsStore for Phase 1.")

    def list_runs(self) -> list[str]:
        raise NotImplementedError("PgStore is a stub; use FsStore for Phase 1.")
