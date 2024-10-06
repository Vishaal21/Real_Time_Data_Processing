from fastapi import FastAPI
from app.router import router
from app.models import Base
from app.database import engine
from app.websocket.websocket_router import router as websocket_router
from fastapi import middleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)
app.include_router(websocket_router)


origins = [
    "https://hoppscotch.io/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)




