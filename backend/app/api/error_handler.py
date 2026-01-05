import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.utils.exceptions.base_app_exception import BaseAppException
from app.utils.exceptions.forbidden_exception import ForbiddenException
from app.utils.exceptions.resource_not_found import ResourceNotFoundException
from app.utils.exceptions.validation_exception import ValidationException
from app.utils.exceptions.road_exception import RoadException
from app.utils.exceptions.settlement_exception import SettlementException
from app.utils.exceptions.setup_exception import SetupException
from app.utils.exceptions.state_not_found_exception import StateNotFoundException


def register_error_handlers(app):
    @app.exception_handler(BaseAppException)
    async def handle_app_error(request: Request, exc: BaseAppException):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

    @app.exception_handler(ResourceNotFoundException)
    async def handle_not_found_error(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"error": exc.message}
        )

    @app.exception_handler(ValidationException)
    async def handle_validation_error(request: Request, exc: ValidationException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.message}
        )

    @app.exception_handler(ForbiddenException)
    async def handle_forbidden_error(request: Request, exc: ForbiddenException):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN, content={"error": exc.message}
        )

    @app.exception_handler(RoadException)
    async def handle_road_error(request: Request, exc: RoadException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.message}
        )

    @app.exception_handler(SettlementException)
    async def handle_settlement_error(request: Request, exc: SettlementException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.message}
        )

    @app.exception_handler(SetupException)
    async def handle_setup_error(request: Request, exc: SetupException):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.message}
        )

    @app.exception_handler(StateNotFoundException)
    async def handle_state_not_found_error(
        request: Request, exc: StateNotFoundException
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"error": exc.message}
        )

    @app.exception_handler(Exception)
    async def handle_generic_error(request: Request, exc: Exception):
        print(
            "\n--- INTERNAL SERVER ERROR ---\n",
            traceback.format_exc(),
            "\n----------------------------\n",
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Internal server error: {str(exc)}"},
        )
