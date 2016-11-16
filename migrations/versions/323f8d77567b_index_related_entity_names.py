"""Index related entity names

Revision ID: 323f8d77567b
Revises: 82b34e2777a4
Create Date: 2016-11-16 13:00:25.782487

"""

# revision identifiers, used by Alembic.
revision = '323f8d77567b'
down_revision = '82b34e2777a4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_related_entity_name'), 'related_entity', ['name'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_related_entity_name'), table_name='related_entity')
    ### end Alembic commands ###
