from pydantic_jsonapi import JsonApiModel
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Header,
    Depends,
    Response,
)
from src.models import model
from src.database import sessionLocal
from src.models.request import EndpointRequest
from src.utils import CustomException

EndpointRequestJson, EndpointResponseJson\
     = JsonApiModel("endpoints", EndpointRequest)

router = APIRouter()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/vnd.api+json"""

    if content_type != "application/vnd.api+json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/vnd.api+json",
        )


@router.get("/endpoints", dependencies=[Depends(application_vnd)])
def read_all(response: Response):
    db = sessionLocal()
    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = db.query(model.Endpoint).all()
    result = [
        EndpointResponseJson.resource_object(
            id=point.id,
            attributes={
                "verb": point.verb,
                "path": point.path,
                "response": {
                    "code": point.code,
                    "headers": point.headers,
                    "body": point.body,
                },
            },
        ) for point in endpoint
    ]
    return {"data": result}


@router.get("/{path_param}", dependencies=[Depends(application_vnd)])
def read_root(path_param: str, response: Response):
    db = sessionLocal()
    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = (db.query(model.Endpoint).filter(
        model.Endpoint.path == f"/{path_param}").first())
    if endpoint is not None:
        return endpoint.body
    else:
        raise CustomException(msg="Requested page", name=f"/{path_param}")


@router.post("/endpoints",
             status_code=201,
             dependencies=[Depends(application_vnd)])
def create_endpoint(req: EndpointRequestJson, response: Response):
    db = sessionLocal()
    response.headers["content-type"] = "application/vnd.api+json"
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
        endpoint = (db.query(model.Endpoint).filter(
            model.Endpoint.path == f"{data.path}").first())
        return EndpointResponseJson(data=EndpointResponseJson.resource_object(
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
        ))

    except Exception:
        raise HTTPException(status_code=409, detail="This path already exists")


@router.patch("/endpoints/{id}",
              status_code=200,
              dependencies=[Depends(application_vnd)])
def update_endpoint(id: int, req: EndpointRequestJson, response: Response):
    db = sessionLocal()
    response.headers["content-type"] = "application/vnd.api+json"
    data = req.data.attributes
    endpoint = db.query(model.Endpoint).filter(model.Endpoint.id == id).first()
    if endpoint is None:
        raise HTTPException(status_code=404,
                            detail="This path does not exists")
    try:
        endpoint.verb = data.verb
        endpoint.path = data.path
        endpoint.code = data.response.code
        endpoint.headers = data.response.headers
        endpoint.body = data.response.body

        db.commit()
    except Exception:
        raise HTTPException(status_code=404,
                            detail="This new path already exists")
    return EndpointResponseJson(data=EndpointResponseJson.resource_object(
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
    ))


@router.delete("/endpoints/{id}",
               status_code=204,
               dependencies=[Depends(application_vnd)])
def delete_endpoint(id: int, response: Response):
    db = sessionLocal()
    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = db.query(
        model.Endpoint).filter(model.Endpoint.id == id).delete()
    db.commit()
    if endpoint == 0:
        raise CustomException(name=id, msg="Requested Endpoint with ID")
