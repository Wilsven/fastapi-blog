"""Add foreign key to posts table

Revision ID: e28528def319
Revises: 98d8478cf5b8
Create Date: 2022-11-07 00:52:03.610566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e28528def319"
down_revision = "98d8478cf5b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
