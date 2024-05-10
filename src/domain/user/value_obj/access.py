from src.domain.common.value_obj.string import StrVO


class AccessToken(StrVO):

    MIN_LEN = 20
    MAX_LEN = 300

    @classmethod
    def _validate(cls, value: str) -> None:
        assert cls.MIN_LEN <= len(value), "Too Short Value"
        assert cls.MAX_LEN >= len(value), "Too Long Value"
