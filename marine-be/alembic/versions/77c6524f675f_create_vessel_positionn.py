"""Create Vessel Positionn

Revision ID: 77c6524f675f
Revises: 
Create Date: 2022-08-25 19:25:52.108407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77c6524f675f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vesselposition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vessel_id', sa.Integer(), nullable=True),
    sa.Column('latitude', sa.Float(precision=12), nullable=True),
    sa.Column('longitude', sa.Float(precision=12), nullable=True),
    sa.Column('position_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_vesselposition_id'), 'vesselposition', ['id'], unique=False)
    op.create_index(op.f('ix_vesselposition_vessel_id'), 'vesselposition', ['vessel_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_vesselposition_vessel_id'), table_name='vesselposition')
    op.drop_index(op.f('ix_vesselposition_id'), table_name='vesselposition')
    op.drop_table('vesselposition')
    # ### end Alembic commands ###
