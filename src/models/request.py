

from pydantic import BaseModel, Json
from enum import Enum


class StringValueRepresentationEnumMixin(str, Enum):
    def __str__(self) -> str:
        return self.value


class VerbTypes(StringValueRepresentationEnumMixin):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"


class Headers(BaseModel):
    key: str
    value: str


class Response(BaseModel):
    code: int
    headers: dict
    body: str


class EndpointRequest(BaseModel):
    verb: VerbTypes
    path: str
    response: Response
