"""empty message

Revision ID: d2982be30530
Revises: f4baa303fb4c
Create Date: 2024-12-01 15:08:30.933289

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d2982be30530"
down_revision: Union[str, None] = "f4baa303fb4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("logsequence_enable", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "logsequence_enable")
    # ### end Alembic commands ###
