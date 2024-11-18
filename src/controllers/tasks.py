from typing import Sequence
from uuid import UUID

from advanced_alchemy.extensions.litestar import SQLAlchemyDTO
from litestar import Controller, get, patch, post, status_codes
from litestar.di import Provide
from litestar.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.attributes import InstrumentedAttribute

from src.dependencies import get_user_id
from src.models import Task
from src.schemas import CreateTaskDTO, PartialDTO


class TasksController(Controller):
    path = '/tasks'
    dependencies = {'user_id': Provide(get_user_id)}

    @get('/', return_dto=SQLAlchemyDTO[Task])
    async def list_tasks(
        self, user_id: int, db_session: AsyncSession, show_completed: bool = True,
    ) -> Sequence[Task]:
        filters = {'user_id': user_id}
        if not show_completed:
            filters['is_completed'] = False

        return (await db_session.execute(select(Task).filter_by(**filters))).scalars().all()

    @post('/', dto=CreateTaskDTO)
    async def create_task(self, user_id: int, data: Task, db_session: AsyncSession) -> Task:
        data.user_id = user_id
        db_session.add(data)
        await db_session.commit()
        await db_session.refresh(data)

        return data

    @get('/{task_id:str}/', return_dto=SQLAlchemyDTO[Task])
    async def get_task(self, user_id: int, task_id: UUID, db_session: AsyncSession) -> Task:
        task = await db_session.get(Task, task_id)
        if task is None or task.user_id != user_id:
            raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND)

        return task

    @patch('/{task_id:str}/', dto=PartialDTO[Task])
    async def complete_task(self, user_id: int, task_id: UUID, db_session: AsyncSession, data: Task) -> Task:
        task = await db_session.get(Task, task_id)
        if task is None or task.user_id != user_id:
            raise HTTPException(status_code=status_codes.HTTP_404_NOT_FOUND)

        for key, value in vars(data).items():
            if hasattr(task, key) and isinstance(getattr(Task, key, None), InstrumentedAttribute):
                setattr(task, key, value)

        await db_session.commit()
        await db_session.refresh(task)

        return task
