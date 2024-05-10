from src.application.book.cases.book_crud import BookCrudCase
from src.domain.book.dto.request import NewBookRequest
from src.infrastructure.persistence.postgres.repositories.book_repo import BookRepo
from src.kernel.rmq.handlers.factory_method import AbstractRmqHandlerCreator
from src.presentation.amqp.handlers.new_book.handler import NewBookHandler


class NewBookHandlerFactory(AbstractRmqHandlerCreator):

    @property
    def __book_repo(self) -> BookRepo:
        return BookRepo(self._db_connection_pools.postgres)

    @property
    def __book_crud(self) -> BookCrudCase:
        return BookCrudCase(self.__book_repo)

    @property
    def __book_model(self) -> NewBookRequest:
        return NewBookRequest(**self._message)

    def create(self) -> NewBookHandler:
        return NewBookHandler(payload=self.__book_model, book_crud=self.__book_crud)
