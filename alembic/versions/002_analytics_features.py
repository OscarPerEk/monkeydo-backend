"""analytics features

Revision ID: 002
Revises: 001
Create Date: 2026-04-25
"""

from alembic import op
import sqlalchemy as sa

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add range columns to lessons
    op.add_column("lessons", sa.Column("range_start_index", sa.Integer, nullable=True))
    op.add_column("lessons", sa.Column("range_end_index", sa.Integer, nullable=True))

    # Drop old CHECK constraint on word_history.status, recreate with 'skipped'
    op.drop_constraint("word_history_status_check", "word_history", type_="check")
    op.create_check_constraint(
        "word_history_status_check",
        "word_history",
        "status IN ('correct', 'ok', 'wrong', 'skipped')",
    )

    # Add composite index for session lookups by lesson
    op.create_index(
        "idx_game_sessions_lesson",
        "game_sessions",
        ["lesson_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("idx_game_sessions_lesson", table_name="game_sessions")

    op.drop_constraint("word_history_status_check", "word_history", type_="check")
    op.create_check_constraint(
        "word_history_status_check",
        "word_history",
        "status IN ('correct', 'ok', 'wrong')",
    )

    op.drop_column("lessons", "range_end_index")
    op.drop_column("lessons", "range_start_index")
