"""making task id nullable

Revision ID: e1dcfea5ad36
Revises: cb94a2d6c7db
Create Date: 2018-08-09 14:53:51.008267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1dcfea5ad36'
down_revision = 'cb94a2d6c7db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('block_task_meta', 'task_id',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('block_task_meta', 'task_id',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###
