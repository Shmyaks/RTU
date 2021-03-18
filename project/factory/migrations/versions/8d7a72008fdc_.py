"""empty message

Revision ID: 8d7a72008fdc
Revises: 
Create Date: 2021-03-18 19:58:44.871329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d7a72008fdc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('factory',
    sa.Column('factory_id', sa.Integer(), nullable=True),
    sa.Column('factory_name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('factory_id')
    )
    op.create_table('crafting',
    sa.Column('craft_id', sa.Integer(), nullable=True),
    sa.Column('factory_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('craft_count', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.Column('product_storage', sa.Integer(), nullable=True),
    sa.Column('interval_delivery', sa.Integer(), nullable=False),
    sa.Column('scheduler_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['factory_id'], ['factory.factory_id'], ),
    sa.PrimaryKeyConstraint('craft_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('crafting')
    op.drop_table('factory')
    # ### end Alembic commands ###
