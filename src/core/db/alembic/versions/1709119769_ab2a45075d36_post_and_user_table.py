"""post and user table

Revision ID: ab2a45075d36
Revises: 49896241fc65
Create Date: 2024-02-28 16:29:29.332829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "ab2a45075d36"
down_revision = "49896241fc65"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "post",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.String(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "post",
        "created_at",
        existing_type=sa.String(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
