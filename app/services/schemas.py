from datetime import datetime, date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    file_open = "file_open"
    image_view = "image_view"
    video_play = "video_play"
    classification_event = "classification_event"


class MediaType(str, Enum):
    image = "image"
    video = "video"
    preview = "preview"


class EventIn(BaseModel):
    timestamp: datetime
    event_type: EventType
    media_type: MediaType
    severity: int = Field(ge=1, le=5)
    duration_seconds: float = Field(ge=0)
    user_identifier: str = Field(min_length=1)
    source_tool: str


class EventsIngestRequest(BaseModel):
    events: list[EventIn]


class WindowMetricOut(BaseModel):
    window_start: date
    T_minutes: float
    E_events: int
    V_volume: float
    D_density: float


class IEOWindowOut(BaseModel):
    window_start: date
    IEO_score: float
    IEO_linear: float
    IEO_sat: float
    z_T: float
    z_E: float
    z_V: float
    z_D: float
