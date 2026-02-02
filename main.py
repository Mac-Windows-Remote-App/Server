from fastapi import FastAPI
from pydantic import BaseModel, Field
from enum import Enum
from typing import Union

app = FastAPI()

class EventType(str, Enum):
    CONN_REQ = "CONN_REQ"
    MOUSE_MOVE = "MOUSE_MOVE"
    TRACKPAD_GESTURE = "TRACKPAD_GESTURE"
    INPUT_ACTION = "INPUT_ACTION"

class RoleType(str, Enum):
    CONTROLLER = "CONTROLLER"
    TARGET = "TARGET"

class OsType(str, Enum):
    MAC = "macOS"
    WINDOWS = "Windows"

class Resolution(BaseModel):
    width: int
    height: int

class ConnPayload(BaseModel):
    device_name: str
    os: OsType
    role: RoleType
    resolution: Resolution

class ConnectionReq(BaseModel):
    event: EventType = Field(..., examples=[EventType.CONN_REQ])
    payload: ConnPayload



