from dataclasses import dataclass
from datetime import datetime


@dataclass
class Resume:
    id: int
    type_id: int
    version: int
    name: str
    created_at: datetime
    updated_at: datetime
