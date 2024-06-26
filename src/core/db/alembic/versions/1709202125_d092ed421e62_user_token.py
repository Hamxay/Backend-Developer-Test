"""USER TOKEN

Revision ID: d092ed421e62
Revises: ab2a45075d36
Create Date: 2024-02-29 15:22:05.506662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d092ed421e62"
down_revision = "ab2a45075d36"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("token", sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "token")
    # ### end Alembic commands ###
