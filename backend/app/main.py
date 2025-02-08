from fastapi import FastAPI, middleware
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.global_exception_filter import global_exception_handler

# from app.websocket.websocket_router import router as websocket_router
from app.routers.file_router import file_router

app = FastAPI()

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(file_router)
# app.include_router(websocket_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
