from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.group_routes import router as group_router
from app.api.sync_routes import router as sync_router

app = FastAPI(
    title="PackVote",
    description="Constraint-Aware Group Travel Planning System"
)

# Allow Frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Relaxed for local dev/Network Error debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(group_router, prefix="/api/v1")
app.include_router(sync_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "PackVote backend running"}
