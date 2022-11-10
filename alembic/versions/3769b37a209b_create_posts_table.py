"""Create posts table

Revision ID: 3769b37a209b
Revises: 
Create Date: 2022-11-06 19:24:25.520572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3769b37a209b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
