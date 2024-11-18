from litestar import Response, get, status_codes

from src.controllers.tasks import TasksController


@get('/health/')
async def health() -> Response:
    return Response(content={}, status_code=status_codes.HTTP_200_OK)


routes = [health, TasksController]
