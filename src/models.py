import datetime
import uuid
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

uuid = Annotated[uuid.UUID, mapped_column(UUID, primary_key=True, default=uuid.uuid4)]  # type: ignore
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)
]
