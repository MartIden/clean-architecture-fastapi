"""init

Revision ID: f16c93586b24
Revises: 
Create Date: 2024-05-01 17:04:22.079704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f16c93586b24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('surname', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authors_id'), 'authors', ['id'], unique=True)
    op.create_index(op.f('ix_authors_name'), 'authors', ['name'], unique=False)
    op.create_index(op.f('ix_authors_surname'), 'authors', ['surname'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('login')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table('tokens',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=True)
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=True)
    op.create_index(op.f('ix_tokens_user_id'), 'tokens', ['user_id'], unique=False)
    op.create_table('books',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('isbn', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_author_id'), 'books', ['author_id'], unique=False)
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=True)
    op.create_index(op.f('ix_books_isbn'), 'books', ['isbn'], unique=True)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    op.create_table('users_books',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=True),
    sa.Column('updated_at', sa.BigInteger(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'book_id', name='user_book_uc')
    )
    op.create_index(op.f('ix_users_books_book_id'), 'users_books', ['book_id'], unique=False)
    op.create_index(op.f('ix_users_books_id'), 'users_books', ['id'], unique=True)
    op.create_index(op.f('ix_users_books_user_id'), 'users_books', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_books_user_id'), table_name='users_books')
    op.drop_index(op.f('ix_users_books_id'), table_name='users_books')
    op.drop_index(op.f('ix_users_books_book_id'), table_name='users_books')
    op.drop_table('users_books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_isbn'), table_name='books')
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_index(op.f('ix_books_author_id'), table_name='books')
    op.drop_table('books')
    op.drop_index(op.f('ix_tokens_user_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_authors_surname'), table_name='authors')
    op.drop_index(op.f('ix_authors_name'), table_name='authors')
    op.drop_index(op.f('ix_authors_id'), table_name='authors')
    op.drop_table('authors')
    # ### end Alembic commands ###
