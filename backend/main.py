from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from core.db import TORTOISE_ORM
from api import analysis, auth, config, progress, project
from fastapi.middleware.cors import CORSMiddleware  # ✅ ADD THIS

app = FastAPI(title="HUE Agent System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(project.router, prefix="/projects", tags=["Projects"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])  # ✅ ADD THIS LINE
app.include_router(progress.router, prefix="/progress", tags=["Progress"])  # ✅ ADD
app.include_router(config.router, prefix="/config", tags=["Configuration"])  

# Register Tortoise ORM
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False, # We use Aerich for migrations
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "HUE Multi-Agent System API is running"}