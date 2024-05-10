from fastapi import Depends


class HealthCheckController(IJsonController):

    def __init__(self, repo: PingRepo = Depends(get_repository(PingRepo))):
        self.__repo = repo

    async def __postgres_ping(self) -> None:
        await self.__repo.ping()

    async def answer(self) -> HealthAnswerDTO:
        await self.__postgres_ping()
        return HealthAnswerDTO(success=True)
