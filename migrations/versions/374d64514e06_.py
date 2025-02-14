"""empty message

Revision ID: 374d64514e06
Revises: bbd0dc823856
Create Date: 2023-08-16 20:48:16.082909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '374d64514e06'
down_revision = 'bbd0dc823856'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'task', 'goal', ['goal_id'], ['goal_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'goal_id')
    # ### end Alembic commands ###
