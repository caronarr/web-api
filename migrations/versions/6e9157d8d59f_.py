"""empty message

Revision ID: 6e9157d8d59f
Revises: 
Create Date: 2018-12-05 12:17:45.406968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e9157d8d59f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_location_latitude'), 'location', ['latitude'], unique=False)
    op.create_index(op.f('ix_location_longitude'), 'location', ['longitude'], unique=False)
    op.create_index(op.f('ix_location_name'), 'location', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('photo', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=True)
    op.create_table('driver_offer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('scheduled_time', sa.DateTime(), nullable=True),
    sa.Column('origin_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.Column('requested_tip', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['driver_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['origin_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rider_offer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rider_id', sa.Integer(), nullable=True),
    sa.Column('scheduled_time', sa.DateTime(), nullable=True),
    sa.Column('origin_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.Column('offered_tip', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['origin_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['rider_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('deal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('driver_offer_id', sa.Integer(), nullable=True),
    sa.Column('rider_offer_id', sa.Integer(), nullable=True),
    sa.Column('agreed_tip', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['driver_offer_id'], ['driver_offer.id'], ),
    sa.ForeignKeyConstraint(['rider_offer_id'], ['rider_offer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deal_driver_offer_id'), 'deal', ['driver_offer_id'], unique=False)
    op.create_index(op.f('ix_deal_rider_offer_id'), 'deal', ['rider_offer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_deal_rider_offer_id'), table_name='deal')
    op.drop_index(op.f('ix_deal_driver_offer_id'), table_name='deal')
    op.drop_table('deal')
    op.drop_table('rider_offer')
    op.drop_table('driver_offer')
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_location_name'), table_name='location')
    op.drop_index(op.f('ix_location_longitude'), table_name='location')
    op.drop_index(op.f('ix_location_latitude'), table_name='location')
    op.drop_table('location')
    # ### end Alembic commands ###
