from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    updated_at: int = int(datetime.now().timestamp())
    created_at: int = int(datetime.now().timestamp())