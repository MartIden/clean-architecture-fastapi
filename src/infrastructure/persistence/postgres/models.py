from sqlalchemy import Boolean, Column, String, BigInteger, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base


class UserModel(declarative_base()):

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    login = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)


class TokenModel(declarative_base()):

    __tablename__ = "tokens"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    expired_at = Column(BigInteger)

    access_token = Column(String, unique=True, index=True)
    is_active = Column(Boolean)
    user_id = Column(Integer, ForeignKey(UserModel.id, ondelete='CASCADE'), index=True)


class AuthorModel(declarative_base()):

    __tablename__ = "authors"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    name = Column(String, index=True)
    surname = Column(String, index=True)


class BookModel(declarative_base()):

    __tablename__ = "books"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    title = Column(String, index=True)
    description = Column(String)
    isbn = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey(AuthorModel.id), index=True)


class UserBookModel(declarative_base()):

    __tablename__ = "users_books"
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='user_book_uc'),
    )

    id = Column(BigInteger, primary_key=True, index=True, unique=True)

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    user_id = Column(Integer, ForeignKey(UserModel.id), index=True)
    book_id = Column(Integer, ForeignKey(BookModel.id), index=True)
