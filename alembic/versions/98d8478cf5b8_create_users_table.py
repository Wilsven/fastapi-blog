"""Create users table

Revision ID: 98d8478cf5b8
Revises: bd3bb90ac750
Create Date: 2022-11-06 19:46:09.159166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "98d8478cf5b8"
down_revision = "bd3bb90ac750"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("users")
