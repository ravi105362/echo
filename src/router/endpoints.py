from fastapi import (
    APIRouter,
    Depends,
    Response,
)
from src.models import model
from src.database import sessionLocal
from src.utils import CustomException, application_vnd,\
     response_object, EndpointRequestJson, EndpointResponseJson
from sqlalchemy.orm import Session
from src.utils import get_logger

router = APIRouter()
logging = get_logger()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/endpoints", dependencies=[Depends(application_vnd)])
async def read_all(response: Response, db: Session = Depends(get_db)):
    """ Returns all the endpoints created """

    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = db.query(model.Endpoint).all()
    result = [response_object(point) for point in endpoint]
    logging.info("Read all fetched")
    return {"data": result}


@router.get("/{path_param}", dependencies=[Depends(application_vnd)])
async def read_root(path_param: str,
                    response: Response,
                    db: Session = Depends(get_db)):
    """ Returns the response for created endpoints """

    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = (db.query(model.Endpoint).filter(
        model.Endpoint.path == f"/{path_param}").first())

    if endpoint is not None:
        for key, value in endpoint.headers.items():
            response.headers[key] = value
        return endpoint.body
    else:
        logging.error(f"Endpoint with path {path_param} not found")
        raise CustomException(msg="Requested page",
                              name=f"/{path_param}",
                              end_msg="does not exists",
                              status=404)


@router.post("/endpoints",
             status_code=201,
             dependencies=[Depends(application_vnd)])
async def create_endpoint(req: EndpointRequestJson,
                          response: Response,
                          db: Session = Depends(get_db)):
    """ Creates the new endpoint """

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
        return EndpointResponseJson(data=response_object(endpoint))

    except Exception:
        logging.error(f"Endpoint with path {data.path} not created")
        raise CustomException(msg="Requested page",
                              name=f"{data.path}",
                              end_msg="already exists",
                              status=409)


@router.patch("/endpoints/{id}",
              status_code=200,
              dependencies=[Depends(application_vnd)])
async def update_endpoint(id: int,
                          req: EndpointRequestJson,
                          res: Response,
                          db: Session = Depends(get_db)):
    """ Updates the created endpoint """

    res.headers["content-type"] = "application/vnd.api+json"
    data = req.data.attributes
    endpoint = db.query(model.Endpoint).filter(model.Endpoint.id == id).first()
    if endpoint is None:
        logging.error(f"Endpoint with id {id} does not exists")
        raise CustomException(msg="Requested page",
                              name=f"{data.path}",
                              end_msg="does not exists",
                              status=404)
    try:
        endpoint.verb = data.verb
        endpoint.path = data.path
        endpoint.code = data.response.code
        endpoint.headers = data.response.headers
        endpoint.body = data.response.body
        db.commit()
    except Exception:
        logging.error(f"Endpoint with id {id} failed to update")
        raise CustomException(msg="Requested page",
                              name=f"{data.path}",
                              end_msg="failed to update",
                              status=409)
    return EndpointResponseJson(data=response_object(endpoint))


@router.delete("/endpoints/{id}",
               status_code=204,
               dependencies=[Depends(application_vnd)])
async def delete_endpoint(id: int,
                          response: Response,
                          db: Session = Depends(get_db)):
    """ Deletes the endpoint created """

    response.headers["content-type"] = "application/vnd.api+json"
    endpoint = db.query(
        model.Endpoint).filter(model.Endpoint.id == id).delete()
    db.commit()
    if endpoint == 0:
        logging.error(f"Endpoint with id {id} does not exists")
        raise CustomException(name=id,
                              msg="Requested Endpoint with ID",
                              end_msg="does not exists",
                              status=404)
