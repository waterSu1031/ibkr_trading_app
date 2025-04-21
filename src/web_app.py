# src/web_app.py

from fastapi import FastAPI
from .routes.webhook import router as webhook_router

web_app = FastAPI()
web_app.include_router(webhook_router)
