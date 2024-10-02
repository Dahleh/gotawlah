"""fix user updated_at

Revision ID: 0a85076952df
Revises: 6432641a983b
Create Date: 2024-10-02 01:33:32.901268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a85076952df'
down_revision: Union[str, None] = '6432641a983b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("users","updated_at")
    pass


def downgrade():
    pass
