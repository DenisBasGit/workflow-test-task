from typing import Optional

from fastapi import status


class WRKFEception(Exception):
    message: str = ""
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    loc: Optional[str] = None

    def __init__(
        self,
        message: Optional[str] = None,
        loc: str | None = None,
    ):
        if loc is not None:
            self.loc = loc

        if message is not None:
            self.message = message

    def __str__(self) -> str:
        return self.message
