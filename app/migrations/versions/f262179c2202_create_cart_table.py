"""Create cart_table

Revision ID: f262179c2202
Revises: d70048634620
Create Date: 2024-01-27 15:53:19.373342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f262179c2202'
down_revision: Union[str, None] = 'd70048634620'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('date_from', sa.Date(), nullable=False),
    sa.Column('date_to', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carts')
    # ### end Alembic commands ###
