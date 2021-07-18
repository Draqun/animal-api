"""Init database

Revision ID: f223b8e02d45
Revises: 
Create Date: 2021-07-04 19:11:09.633682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f223b8e02d45'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'animals',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Unicode(1024))
    )


def downgrade():
    op.drop_table('animals')
