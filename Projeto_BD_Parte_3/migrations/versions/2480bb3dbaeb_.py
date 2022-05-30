"""empty message

Revision ID: 2480bb3dbaeb
Revises: ef28d9cb1c6a
Create Date: 2022-05-29 15:20:57.432140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2480bb3dbaeb'
down_revision = 'ef28d9cb1c6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('possui',
    sa.Column('evento_id', sa.Integer(), nullable=True),
    sa.Column('categoria_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categoria_id'], ['categorias.id'], ),
    sa.ForeignKeyConstraint(['evento_id'], ['eventos.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('possui')
    # ### end Alembic commands ###