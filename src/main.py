import json
from pydantic_jsonapi import JsonApiModel
from typing import Union
from fastapi import FastAPI, HTTPException, status, Header, Request, Depends
from fastapi.responses import JSONResponse
from src.models import model
from src.database import engine, sessionLocal
from src.models.request import EndpointRequest
import src.models

app = FastAPI()

EndpointRequestJson, EndpointResponseJson = JsonApiModel("endpoints", EndpointRequest)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


model.Base.metadata.create_all(bind=engine)


def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/vnd.api+json"""

    if content_type != "application/vnd.api+json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/vnd.api+json",
        )


class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=404,
        content={
            "errors": [
                {
                    "code": "not_found",
                    "detail": f"Requested page `/{exc.name}` does not exist",
                }
            ],
        },
    )


@app.get("/endpoints")
def read_all():
    db = sessionLocal()
    endpoint = db.query(model.Endpoint).all()
    return {"endpoint": endpoint}


@app.get("/{path_param}", dependencies=[Depends(application_vnd)])
def read_root(path_param: str):
    db = sessionLocal()
    endpoint = (
        db.query(model.Endpoint).filter(model.Endpoint.path == f"/{path_param}").first()
    )
    if endpoint is not None:
        return EndpointResponseJson(
            data=EndpointResponseJson.resource_object(
                id=endpoint.id,
                attributes={
                    "verb": endpoint.verb,
                    "path": endpoint.path,
                    "response": {
                        "code": endpoint.code,
                        "headers": endpoint.headers,
                        "body": endpoint.body,
                    },
                },
            )
        )
    else:
        raise CustomException(name=path_param)


@app.post("/endpoints", status_code=201, dependencies=[Depends(application_vnd)])
def create_endpoint(req: EndpointRequestJson):
    db = sessionLocal()
    data = req.data.attributes
    try:
        to_add = model.Endpoint(
            verb=data.verb,
            path=data.path,
            code=data.response.code,
            headers=data.response.headers,
            body=data.response.body,
        )
        db.add(to_add)
        db.commit()
        endpoint = (
            db.query(model.Endpoint)
            .filter(model.Endpoint.path == f"{data.path}")
            .first()
        )
        return EndpointResponseJson(
            data=EndpointResponseJson.resource_object(
                id=endpoint.id,
                attributes={
                    "verb": endpoint.verb,
                    "path": endpoint.path,
                    "response": {
                        "code": endpoint.code,
                        "headers": endpoint.headers,
                        "body": endpoint.body,
                    },
                },
            )
        )

    except Exception as exc:
        raise HTTPException(status_code=409, detail="This path already exists")


@app.patch("/endpoints/{id}", status_code=200, dependencies=[Depends(application_vnd)])
def update_endpoint(id: int, req: EndpointRequestJson):
    db = sessionLocal()
    data = req.data.attributes
    endpoint = db.query(model.Endpoint).filter(model.Endpoint.id == id).first()
    if endpoint is None:
        raise HTTPException(status_code=404, detail="This path does not exists")

    endpoint.verb = data.verb
    endpoint.path = data.path
    endpoint.code = data.response.code
    endpoint.headers = data.response.headers
    endpoint.body = data.response.body

    db.commit()
    return EndpointResponseJson(
        data=EndpointResponseJson.resource_object(
            id=endpoint.id,
            attributes={
                "verb": endpoint.verb,
                "path": endpoint.path,
                "response": {
                    "code": endpoint.code,
                    "headers": endpoint.headers,
                    "body": endpoint.body,
                },
            },
        )
    )


@app.delete("/endpoints/{id}", status_code=204, dependencies=[Depends(application_vnd)])
def delete_endpoint(id: int):
    db = sessionLocal()
    endpoint = db.query(model.Endpoint).filter(model.Endpoint.id == id).delete()
    if endpoint == 0:
        raise HTTPException(status_code=404, detail="This path does not exists")
