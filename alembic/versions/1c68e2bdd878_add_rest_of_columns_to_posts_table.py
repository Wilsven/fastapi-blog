"""Add rest of columns to posts table

Revision ID: 1c68e2bdd878
Revises: e28528def319
Create Date: 2022-11-08 00:29:21.482326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1c68e2bdd878"
down_revision = "e28528def319"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.Boolean,
            server_default="TRUE",
            nullable=False,
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
