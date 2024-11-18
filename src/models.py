from uuid import UUID

from sqlalchemy import func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    user_id: Mapped[int]
    title: Mapped[str]
    description: Mapped[str | None] = None
    is_completed: Mapped[bool] = mapped_column(server_default=text('false'))
