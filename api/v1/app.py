#!/usr/bin/python3
"""Poll API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database_config import engine
from .models import Base
from .routes import poll_router
from api.v1.users.user_routes import user_router
from api.v1.bans.ban_routes import ban_router
from api.v1.choices.choice_route import choice_router

Base.metadata.create_all(bind=engine)
app = FastAPI(
    debug=True, root_path="/",
    openapi_tags=["Poll API"]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


@app.get("/")
async def index():
    """Poll API."""
    return {"message": "Poll API"}

app.include_router(user_router)
app.include_router(ban_router)
app.include_router(poll_router)
app.include_router(choice_router)
