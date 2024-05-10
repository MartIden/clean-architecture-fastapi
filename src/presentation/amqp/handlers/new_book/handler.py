from src.application.book.cases.book_crud import BookCrudCase
from src.domain.book.dto.new_book import NewBook
from src.domain.book.dto.request import NewBookRequest
from src.kernel.rmq.handlers.abstract_handler import AbstractRmqHandler


class NewBookHandler(AbstractRmqHandler):

    def __init__(self, payload: NewBookRequest, book_crud: BookCrudCase):
        self.__payload = payload
        self.__book_crud = book_crud

    async def handle(self) -> None:
        book = await self.__book_crud.create(NewBook(**self.__payload.model_dump()))
        self._log_handler(message="Book Is Created", extra={"book": book.model_dump()})
