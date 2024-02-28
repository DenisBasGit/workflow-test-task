import datetime
from typing import Annotated
import uuid

from sqlalchemy import text
from sqlalchemy.orm import mapped_column

uuid = Annotated[str, mapped_column(primary_key=True, default=uuid.uuid4())]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)
]