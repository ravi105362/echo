import os
from fastapi import Header, HTTPException, status
from src.models.request import EndpointRequest
from pydantic_jsonapi import JsonApiModel
import logging
from src import settings
from dataclasses import dataclass

EndpointRequestJson, EndpointResponseJson\
     = JsonApiModel("endpoints", EndpointRequest)


class CustomException(Exception):

    def __init__(self, name: str, msg: str, end_msg: str, status: int):
        self.name = name
        self.msg = msg
        self.end_msg = end_msg
        self.status = status


def response_object(point):
    return EndpointResponseJson.resource_object(
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
    )


def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/vnd.api+json"""

    if content_type != "application/vnd.api+json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/vnd.api+json",
        )


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename=os.path.join(settings.LOGGER_FOLDER),
        format="%(asctime)s :: %(levelname)s :: %(message)s",
    )
    return logging


@dataclass
class ResponseModel:
    id: int
    verb: str
    path: str
    code: int
    headers: dict
    body: str
