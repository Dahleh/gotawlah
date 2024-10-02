"""fix images

Revision ID: e6059bb3f9aa
Revises: 450ef26642b9
Create Date: 2024-10-02 11:11:34.504662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6059bb3f9aa'
down_revision: Union[str, None] = '450ef26642b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column("resturants", "Images")
    op.add_column("resturants", sa.Column("Images", sa.ARRAY(sa.String), server_default="{}"))
    pass


def downgrade():
    op.drop_column("resturants", "Images")
    pass
