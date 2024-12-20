"""empty message

Revision ID: 43b51052938e
Revises: d2982be30530
Create Date: 2024-12-01 16:24:41.751425

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "43b51052938e"
down_revision: Union[str, None] = "d2982be30530"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("logsequence_message", sa.Column("text", sa.String(), nullable=False))
    op.drop_column("logsequence_message", "message")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "logsequence_message",
        sa.Column("message", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_column("logsequence_message", "text")
    # ### end Alembic commands ###
