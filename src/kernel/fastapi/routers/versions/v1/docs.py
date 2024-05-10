from fastapi import APIRouter

from src.presentation.http.endpoints.api.docs.router import docs_api

""" API ROUTER """
docs_router = APIRouter()
docs_router.include_router(docs_api)
