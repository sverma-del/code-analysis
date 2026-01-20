import os
import zipfile
import io
import re
import requests
from fastapi import HTTPException, UploadFile
from models.projects import Project, SourceType
from models.users import User

UPLOAD_DIR = "storage/uploads"
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Extensions that count as "recognizable code"
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.c', '.cpp', '.h', '.hpp', 
    '.java', '.go', '.rs', '.php', '.rb', '.pyw', '.html', '.css', '.sql'
}

os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_code_file(filename: str) -> bool:
    return any(filename.endswith(ext) for ext in CODE_EXTENSIONS)

async def create_project_from_file(name: str, file: UploadFile, personas: list, user: User):
    # 1. Wrong file formats (Check extension)
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Invalid format. Please upload a .zip file (RAR/7z not supported).")

    # 2. Files that are too large
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 100MB.")

    # 3. Corrupted or incomplete ZIP files
    try:
        zip_buffer = io.BytesIO(content)
        if not zipfile.is_zipfile(zip_buffer):
            raise HTTPException(status_code=400, detail="The file is not a valid ZIP archive.")
        
        with zipfile.ZipFile(zip_buffer) as z:
            # Check for corruption
            if z.testzip() is not None:
                raise HTTPException(status_code=400, detail="ZIP file is corrupted.")
            
            # 4. Empty repositories or non-code repositories
            file_list = z.namelist()
            if not file_list:
                raise HTTPException(status_code=400, detail="The ZIP file is empty.")
            
            # Count code files
            code_files = [f for f in file_list if is_code_file(f)]
            if not code_files:
                raise HTTPException(
                    status_code=400, 
                    detail="No recognizable code found. System supports Python, JS, TS, Java, etc."
                )

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Malformed ZIP file.")

    # Save logic...
    project = await Project.create(
        name=name, user=user, source_type=SourceType.ZIP, personas=personas
    )
    file_path = os.path.join(UPLOAD_DIR, f"{project.id}.zip")
    with open(file_path, "wb") as f:
        f.write(content)
    
    project.file_path = file_path
    await project.save()
    return project

async def create_project_from_github(name: str, github_url: str, personas: list, user: User):
    # 1. Validate GitHub URL format
    # Matches https://github.com/owner/repo
    github_url = github_url.rstrip("/")
    match = re.match(r"https://github\.com/([\w\-\.]+)/([\w\-\.]+)", github_url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL format.")
    
    owner, repo = match.groups()
    # GitHub's "zipball" API redirects to the default branch (main/master)
    download_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"

    # 2. Download the repository content
    try:
        # Use stream=True to check size before full download if needed
        response = requests.get(download_url, stream=True, timeout=15)
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found or is private.")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download from GitHub.")

        content = response.content # Downloads the ZIP into memory
        
        # 3. Size Validation
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="Repository too large for analysis.")

    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to connect to GitHub: {str(e)}")

    # 4. ZIP Validation (Same as create_project_from_file)
    try:
        zip_buffer = io.BytesIO(content)
        if not zipfile.is_zipfile(zip_buffer):
            raise HTTPException(status_code=400, detail="Downloaded content is not a valid ZIP.")
        
        with zipfile.ZipFile(zip_buffer) as z:
            if z.testzip() is not None:
                raise HTTPException(status_code=400, detail="Downloaded ZIP is corrupted.")
            
            file_list = z.namelist()
            code_files = [f for f in file_list if is_code_file(f)]
            
            if not code_files:
                raise HTTPException(
                    status_code=400, 
                    detail="No recognizable code found in the repository."
                )

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Malformed ZIP received from GitHub.")

    # 5. Database and Storage Logic
    project = await Project.create(
        name=name, 
        user=user, 
        source_type=SourceType.GITHUB, 
        github_url=github_url, 
        personas=personas
    )
    
    # Save the file as {project_id}.zip so the background agent finds it exactly like an upload
    file_path = os.path.join(UPLOAD_DIR, f"{project.id}.zip")
    with open(file_path, "wb") as f:
        f.write(content)
    
    project.file_path = file_path
    await project.save()
    
    return project