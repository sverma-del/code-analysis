from pydantic import BaseModel, HttpUrl
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from models.projects import SourceType, ProjectStatus

class ProjectCreateResponse(BaseModel):
    id: UUID
    name: str
    source_type: SourceType
    status: ProjectStatus
    personas: List[str]
    created_at: datetime
    
    # --- MILESTONE 2: Intelligence Fields ---
    detected_framework: Optional[str] = "Unknown"
    detected_language: Optional[str] = "Unknown"
    endpoint_count: int = 0
    file_count: int = 0
    error_message: Optional[str] = None

    class Config:
        from_attributes = True