"""analysis_input_filters

Revision ID: 93a04c1fb3a7
Revises: cd65935c6d98
Create Date: 2023-12-06 16:54:05.410937

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '93a04c1fb3a7'
down_revision = 'cd65935c6d98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'obj_analyses',
        sa.Column(
            'input_filters', sqlalchemy_utils.types.json.JSONType(), nullable=True
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('obj_analyses', 'input_filters')
    # ### end Alembic commands ###
