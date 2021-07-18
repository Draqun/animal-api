"""empty message

Revision ID: cca2ab489b1f
Revises: f223b8e02d45
Create Date: 2021-07-18 13:09:30.697245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cca2ab489b1f'
down_revision = 'f223b8e02d45'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('animals', sa.Column('image_url', sa.String(128)))


def downgrade():
    op.drop_column('animals', 'image_url')
