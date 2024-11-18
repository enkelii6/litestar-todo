from litestar import status_codes
from litestar.exceptions import HTTPException


async def get_user_id(headers: dict[str, str]) -> int:
    try:
        return int(headers['x-user-id'])
    except KeyError:
        raise HTTPException(status_code=status_codes.HTTP_401_UNAUTHORIZED)
