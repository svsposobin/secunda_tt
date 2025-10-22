from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


async def single_exception_handler(
        request: Request,  # noqa
        exception: Exception,
) -> JSONResponse:
    """
        Общий упрощенный централизованный 'хендлер' ошибок
        Можно сделать error-маппинг и разбить по типам
    """
    match exception:
        case ValidationError() | RequestValidationError() as error:
            error_message: str = "Ошибка валидации"
            error_detail: str = str(error)
            status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY

        case SQLAlchemyError() as error:
            error_message = "Ошибка базы данных"
            error_detail = str(error)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        case HTTPException() as error:
            error_message = "Внутренняя ошибка запроса"
            error_detail = str(error.detail)
            status_code = error.status_code

        case Exception() as error:
            error_message = "Ошибка сервера"
            error_detail = str(error)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return JSONResponse(
        status_code=status_code,  # noqa
        content={
            "error": error_message,  # noqa
            "details": error_detail  # noqa
        }
    )
