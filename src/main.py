from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.models import model
from src.database import engine
from src.router import endpoints
from src.utils import CustomException

app = FastAPI()

model.Base.metadata.create_all(bind=engine)
app.include_router(endpoints.router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    headers = {"content-type": "application/vnd.api+json"}
    return JSONResponse(
        status_code=404,
        content={
            "errors": [
                {
                    "code": "not_found",
                    "detail": f"{exc.msg} `{exc.name}` does not exist",
                }
            ],
        },
        headers=headers,
    )
