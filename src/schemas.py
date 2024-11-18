from litestar.plugins.sqlalchemy import SQLAlchemyDTO, SQLAlchemyDTOConfig

from src.models import Task


class ExcludeIdDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id'})


class ExcludeIdAndTimestampsDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(exclude={'id', 'created_at', 'updated_at'})


class PartialDTO(SQLAlchemyDTO):
    config = SQLAlchemyDTOConfig(partial=True)


class CreateTaskDTO(SQLAlchemyDTO[Task]):
    config = SQLAlchemyDTOConfig(exclude={'user_id', 'id', 'is_completed'})
