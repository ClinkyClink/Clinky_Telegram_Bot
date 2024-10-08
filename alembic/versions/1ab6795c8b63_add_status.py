"""add status

Revision ID: 1ab6795c8b63
Revises: 5efe9f115081
Create Date: 2024-06-21 21:09:56.586052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ab6795c8b63'
down_revision: Union[str, None] = '5efe9f115081'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('status', sa.String(length=30), server_default='No data', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'status')
    # ### end Alembic commands ###
