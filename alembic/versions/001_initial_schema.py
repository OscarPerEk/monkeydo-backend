"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-04-05
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "001"
down_revision = None
branch_labels = None
depends_on = None

DEFAULT_USER_ID = "00000000-0000-0000-0000-000000000001"


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.Text, unique=True, nullable=False),
        sa.Column("is_premium", sa.Boolean, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "folders",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "lessons",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("folder_id", UUID(as_uuid=True), sa.ForeignKey("folders.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("text_source", sa.Text, nullable=False),
        sa.Column("target_data", JSONB, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "game_sessions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("lesson_id", UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("difficulty", sa.Text, sa.CheckConstraint("difficulty IN ('easy', 'medium', 'hard')"), nullable=True),
        sa.Column("duration_seconds", sa.Integer, sa.CheckConstraint("duration_seconds BETWEEN 60 AND 600"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "word_history",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("session_id", UUID(as_uuid=True), sa.ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("word_index", sa.Integer, nullable=False),
        sa.Column("typed_word", sa.Text, nullable=False),
        sa.Column("status", sa.Text, sa.CheckConstraint("status IN ('correct', 'ok', 'wrong')"), nullable=True),
        sa.Column("attempts", sa.Integer, server_default="1"),
        sa.Column("latency_ms", sa.Integer, nullable=False),
    )

    op.create_table(
        "analytics_tips",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("session_id", UUID(as_uuid=True), sa.ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("category", sa.Text, sa.CheckConstraint("category IN ('grammar', 'vocab', 'nuance')"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    # Indexes
    op.create_index("idx_users_active", "users", ["id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_folders_active_user", "folders", ["user_id"], postgresql_where=sa.text("deleted_at IS NULL"))
    op.create_index("idx_lessons_home", "lessons", ["user_id"], postgresql_where=sa.text("folder_id IS NULL AND deleted_at IS NULL"))
    op.create_index("idx_lessons_folder", "lessons", ["folder_id"], postgresql_where=sa.text("folder_id IS NOT NULL AND deleted_at IS NULL"))
    op.create_index("idx_word_history_session_lookup", "word_history", ["session_id"])
    op.create_index("idx_game_sessions_user_history", "game_sessions", ["user_id", "created_at"])

    # Seed default user
    op.execute(
        f"""
        INSERT INTO users (id, email, is_premium)
        VALUES ('{DEFAULT_USER_ID}', 'default@monkeydo.app', false)
        ON CONFLICT DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_table("analytics_tips")
    op.drop_table("word_history")
    op.drop_table("game_sessions")
    op.drop_table("lessons")
    op.drop_table("folders")
    op.drop_table("users")
