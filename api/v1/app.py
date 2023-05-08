#!/usr/bin/python3
"""Poll API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from api.v1.users.user_routes import user_router
from api.v1.bans.ban_routes import ban_router
from api.v1.choices.choice_route import choice_router
from api.v1.votes.vote_routes import vote_router
from api.v1.polls.poll_routes import poll_router
from .database_config import engine
from .models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(
    debug=True, root_path="/",
    openapi_tags=["Poll API"],
    docs_url=None, redoc_url=None,
    openapi_url=None
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


@app.get("/api")
async def index():
    """Poll API."""
    return {"message": "Poll API"}


@app.get("/openapi.json")
async def get_open_api_endpoint():
    """Retrieve openapi endpoint."""
    return JSONResponse(
        get_openapi(
            title="PollAPI",
            version=1,
            routes=app.routes
        )
    )


@app.get("/docs")
async def get_documentation():
    """Retrieve documentation."""
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

app.include_router(user_router)
app.include_router(ban_router)
app.include_router(poll_router)
app.include_router(choice_router)
app.include_router(vote_router)
