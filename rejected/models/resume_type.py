from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResumeType:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
