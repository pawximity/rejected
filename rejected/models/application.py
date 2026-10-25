from dataclasses import dataclass
from datetime import datetime


@dataclass
class Application:
    id: int
    company: str
    role: str
    applied_at: datetime
    resume_id: int
    source: str
    created_at: datetime
    updated_at: datetime
