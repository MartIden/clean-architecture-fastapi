from fastapi import Depends

from src.domain.book.dto.request import NewBookRequest
from src.domain.user.dto.response import UserJsonResponse
from src.kernel.fastapi.controller import IJsonController

from src.presentation.amqp.publishers.new_book import NewBookPublisher
from src.presentation.http.depends.publisher import get_publisher


class BookManyTaskCreatorController(IJsonController):

    def __init__(
        self,
        books: list[NewBookRequest],
        publisher: NewBookPublisher = Depends(get_publisher(NewBookPublisher)),

    ):
        self.__books = books
        self.__publisher = publisher

    async def __publish_message(self, book: NewBookRequest) -> None:
        await self.__publisher.publish_model(book)

    def __log_error(self, err: Exception, book: NewBookRequest) -> None:
        self._log_controller(message=str(err), extra={"book": book.model_dump()})

    @staticmethod
    def __create_answer() -> UserJsonResponse:
        return UserJsonResponse(success=True)

    async def answer(self) -> UserJsonResponse:
        for book in self.__books:
            try:
                await self.__publish_message(book)
            except Exception as err:
                self.__log_error(err, book)

        return self.__create_answer()
