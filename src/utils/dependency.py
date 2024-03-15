from typing import Annotated

from fastapi import Depends

from src.utils.unitofwork import UnitOfWork, UnitOfWorkBase

UOWDep = Annotated[UnitOfWorkBase, Depends(UnitOfWork)]
