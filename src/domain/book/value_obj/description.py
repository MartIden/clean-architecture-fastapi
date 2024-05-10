from src.domain.common.value_obj.string import StrVO


class Description(StrVO):
    MIN_LEN = 5
    MAX_LEN = 1000

    @classmethod
    def _validate(cls, value: str) -> None:
        assert cls.MIN_LEN <= len(value), "Too Short Value"
        assert cls.MAX_LEN >= len(value), "Too Long Value"
