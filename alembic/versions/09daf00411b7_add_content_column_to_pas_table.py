"""add content column to pas table

Revision ID: 09daf00411b7
Revises: 56456cbbb469
Create Date: 2023-09-10 17:31:03.445213

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '09daf00411b7'
down_revision: Union[str, None] = '56456cbbb469'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
