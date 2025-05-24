# src/web_app.py

from fastapi import FastAPI
from src.trading.webhook import router as webhook_router
from src.router.router import router as webapp_router

web_app = FastAPI()
web_app.include_router(webhook_router)
web_app.include_router(webapp_router)
