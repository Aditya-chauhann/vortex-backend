from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, communities, posts, votes, comments

app = FastAPI(
    title="Vortex API",
    description="Vortex - A community platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(communities.router)
app.include_router(posts.router)
app.include_router(votes.router)
app.include_router(comments.router)

@app.on_event("startup")
def run_migrations():
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@app.get("/")
def root():
    return {"message": "Vortex API is running"}