"""Add content column to posts table

Revision ID: bd3bb90ac750
Revises: 3769b37a209b
Create Date: 2022-11-06 19:32:57.054264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bd3bb90ac750"
down_revision = "3769b37a209b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
