import uuid
from enum import Enum
from tortoise import fields, models

class SourceType(str, Enum):
    ZIP = "zip"
    GITHUB = "github"

class ProjectStatus(str, Enum):
    INITIALIZED = "initialized"
    PREPROCESSING = "preprocessing"           # Added
    PREPROCESSING_COMPLETE = "preprocessing_complete"  # Added
    READY_FOR_AGENTS = "ready_for_agents"     # Added
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Project(models.Model):
    # Using UUID for the "unique identifier" requirement
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=255)
    
    # Relationship to the User
    user = fields.ForeignKeyField("models.User", related_name="projects")
    
    source_type = fields.CharEnumField(SourceType)
    github_url = fields.CharField(max_length=500, null=True)
    file_path = fields.CharField(max_length=500, null=True)  # Local path to ZIP
    
    # Store selected personas as a list: ["SDE", "PM"]
    personas = fields.JSONField() 
    
    status = fields.CharEnumField(ProjectStatus, default=ProjectStatus.INITIALIZED, max_length=50)
    
    # Milestone 1: Error tracking for invalid files
    error_message = fields.TextField(null=True)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    detected_framework = fields.CharField(max_length=100, null=True)
    detected_language = fields.CharField(max_length=100, null=True)
    endpoint_count = fields.IntField(default=0)
    file_count = fields.IntField(default=0)
    analysis_summary = fields.JSONField(null=True) # For "Found X classes, Y functions"

    class Meta:
        table = "projects"

    def __str__(self):
        return f"{self.name} ({self.id})"
    



class FileMetadata(models.Model):
    id = fields.IntField(pk=True)
    project = fields.ForeignKeyField("models.Project", related_name="files")
    file_path = fields.CharField(max_length=500)
    file_name = fields.CharField(max_length=255)
    extension = fields.CharField(max_length=20)
    size = fields.IntField()
    is_entry_point = fields.BooleanField(default=False)
    content_summary = fields.TextField(null=True) # AI generated brief

    # ✅ ADD THESE NEW FIELDS BELOW:
    imports = fields.JSONField(null=True)  # List of import statements
    exports = fields.JSONField(null=True)  # List of exported classes/functions
    contains_api_routes = fields.BooleanField(default=False)
    contains_db_models = fields.BooleanField(default=False)
    contains_auth = fields.BooleanField(default=False)
    complexity_score = fields.IntField(null=True)  # Cyclomatic complexity
    
    class Meta:
        table = "filemetadata"

class CodeChunk(models.Model):
    id = fields.IntField(pk=True)
    project = fields.ForeignKeyField("models.Project", related_name="chunks")
    file_metadata = fields.ForeignKeyField("models.FileMetadata", related_name="chunks")
    content = fields.TextField()
    chunk_type = fields.CharField(max_length=50) # "function", "class", "module"
    start_line = fields.IntField()
    end_line = fields.IntField()
    # Note: Vector embedding will be handled by pgvector directly via SQL 
        # Add this as a placeholder so Aerich detects a change
    embedding = fields.TextField(null=True) 
    # or a dedicated vector field if using a supporting library.