from fastapi import APIRouter

from src.presentation.http.endpoints.webhook.book.router import book_task_webhook

""" API ROUTER """
webhook_router = APIRouter(prefix="/webhook/v1")

webhook_router.include_router(book_task_webhook)
