"""add_new_table_user_problem_score

Revision ID: a73a81aa9369
Revises: 6a502d45f70f
Create Date: 2025-01-19 20:42:02.009365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a73a81aa9369'
down_revision = '6a502d45f70f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_problem_score',
    sa.Column('ups_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('problemid', sa.Integer(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('AC', 'WA', 'TLE', 'CE', 'OTHER', name='submission_status'), nullable=False),
    sa.ForeignKeyConstraint(['problemid'], ['problem.problemid'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.userid'], ),
    sa.PrimaryKeyConstraint('ups_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_problem_score')
    # ### end Alembic commands ###
