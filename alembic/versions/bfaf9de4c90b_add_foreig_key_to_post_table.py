"""add foreig-key to post table

Revision ID: bfaf9de4c90b
Revises: 45bdc824cd0b
Create Date: 2023-09-10 17:48:58.878767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bfaf9de4c90b'
down_revision: Union[str, None] = '45bdc824cd0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
