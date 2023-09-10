"""Create posts table

Revision ID: 56456cbbb469
Revises: 
Create Date: 2023-09-10 17:16:09.963267

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '56456cbbb469'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('title', sa.String, nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
