"""add parentID to categories

Revision ID: 6432641a983b
Revises: 06878b278786
Create Date: 2024-10-01 18:26:27.870491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6432641a983b'
down_revision: Union[str, None] = '06878b278786'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('categories', sa.Column('parent_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('categories', 'parent_id')
    # ### end Alembic commands ###
