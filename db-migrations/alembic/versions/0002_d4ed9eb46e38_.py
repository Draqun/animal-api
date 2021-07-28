"""empty message

Revision ID: d4ed9eb46e38
Revises: cca2ab489b1f
Create Date: 2021-07-28 20:13:01.906588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4ed9eb46e38'
down_revision = 'cca2ab489b1f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('animals', 'image_url')
    op.add_column('animals', sa.Column('image_url', sa.String(4096)))


def downgrade():
    op.add_column('animals', sa.Column('image_url', sa.String(128)))
    op.drop_column('animals', 'image_url')

