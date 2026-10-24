from dataclasses import dataclass
from datetime import datetime

from rejected.models.resume_type import ResumeType


@dataclass
class Resume:
    id: int
    type: ResumeType
    version: int
    name: str
    created_at: datetime
    updated_at: datetime
