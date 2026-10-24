from dataclasses import dataclass
from datetime import datetime

from rejected.models.resume import Resume


@dataclass
class Application:
    id: int
    company: str
    role: str
    applied_at: datetime
    resume: Resume
    source: str
    created_at: datetime
    updated_at: datetime
