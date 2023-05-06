#!/usr/bin/python3
"""Poll API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database_cofig import engine
from .models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)


@app.get("/api/v1", tags=["Poll API"])
async def index():
    """Poll API."""
    return {"message": "Poll API"}
