from src.infrastructure.persistence.postgres.models import UserModel, TokenModel, BookModel, UserBookModel, AuthorModel

bases = [
    AuthorModel.metadata,
    UserModel.metadata,
    TokenModel.metadata,
    BookModel.metadata,
    UserBookModel.metadata,
]
