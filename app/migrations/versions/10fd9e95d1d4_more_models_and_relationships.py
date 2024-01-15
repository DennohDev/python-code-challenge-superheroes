"""More models and relationships

Revision ID: 10fd9e95d1d4
Revises: fc8dc1006f56
Create Date: 2024-01-15 01:35:46.441015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fd9e95d1d4'
down_revision = 'fc8dc1006f56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('power',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hero_power',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('strength', sa.String(length=255), nullable=False),
    sa.Column('hero_id', sa.Integer(), nullable=False),
    sa.Column('power_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hero_id'], ['hero.id'], ),
    sa.ForeignKeyConstraint(['power_id'], ['power.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('super_name', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hero', schema=None) as batch_op:
        batch_op.drop_column('super_name')
        batch_op.drop_column('name')

    op.drop_table('hero_power')
    op.drop_table('power')
    # ### end Alembic commands ###