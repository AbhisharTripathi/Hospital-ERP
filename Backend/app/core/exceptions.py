import logging

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status
)

from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def register_exception_handlers(
    app: FastAPI
):
    """
    Register all global exception handlers.
    """

    # ----------------------------
    # HTTP Exceptions
    # ----------------------------

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail
            }
        )

    # ----------------------------
    # Validation Errors
    # ----------------------------

    @app.exception_handler(
        RequestValidationError
    )
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Validation Error",
                "errors": exc.errors()
            }
        )

    # ----------------------------
    # Unexpected Exceptions
    # ----------------------------

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):

        logger.exception(exc)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal Server Error"
            }
        )