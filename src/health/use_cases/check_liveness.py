from src.core.use_cases import UseCase, UseCaseHandler


class CheckLiveness(UseCase):
    class Handler(UseCaseHandler["CheckLiveness", bool]):
        async def execute(self, use_case: "CheckLiveness") -> bool:
            return True
