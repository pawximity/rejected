from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplicationEvent:
    id: int
    application_id: int
    event_type: str
    occurred_at: str
    notes: str
    created_at: datetime
    updated_at: datetime
