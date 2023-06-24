from fastapi import FastAPI, Request
from src.models import model
from src.database import engine
from src.router import endpoints
from src.utils import CustomException
from fastapi.responses import JSONResponse

app = FastAPI()

model.Base.metadata.create_all(bind=engine)
app.include_router(endpoints.router)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    headers = {"content-type": "application/vnd.api+json"}
    return JSONResponse(
        status_code=exc.status,
        content={
            "errors": [{
                "code": "not_found",
                "detail": f"{exc.msg} `{exc.name}` {exc.end_msg}",
            }],
        },
        headers=headers,
    )
