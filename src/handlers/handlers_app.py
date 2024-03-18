from typing import TYPE_CHECKING

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.core import app
from src.exceptions import WRKFEception

if TYPE_CHECKING:
    from pydantic.error_wrappers import ErrorDict


def convert_error(err: "ErrorDict") -> dict[str, str]:
    error = {"message": err.get("msg", "Internal error")}

    if "loc" in err and isinstance(err["loc"], (list, tuple)):
        error["field"] = ".".join(map(str, err["loc"]))

    return error


@app.exception_handler(WRKFEception)
async def wr_exception_handler(request: Request, exc: WRKFEception) -> JSONResponse:
    content = {
        "message": exc.message,
    }

    if exc.loc:
        content["field"] = exc.loc

    return JSONResponse(status_code=exc.status_code, content=[content])


@app.exception_handler(ValidationError)
async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=list(map(convert_error, exc.errors())),
    )
