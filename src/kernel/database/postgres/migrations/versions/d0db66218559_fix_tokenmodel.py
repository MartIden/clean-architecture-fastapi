"""fix TokenModel

Revision ID: d0db66218559
Revises: f16c93586b24
Create Date: 2024-05-02 20:39:59.585372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0db66218559'
down_revision = 'f16c93586b24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tokens_user_id_fkey', 'tokens', type_='foreignkey')
    op.create_foreign_key(None, 'tokens', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tokens', type_='foreignkey')
    op.create_foreign_key('tokens_user_id_fkey', 'tokens', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###