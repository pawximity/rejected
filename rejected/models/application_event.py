from dataclasses import dataclass
from datetime import datetime

from rejected.models.application import Application


@dataclass
class ApplicationEvent:
    id: int
    application: Application
    event_type: str
    occurred_at: datetime
    notes: str
    created_at: datetime
    updated_at: datetime
