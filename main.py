from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routes.users import user_route
from routes.events import event_route

from database.connection import Settings

app = FastAPI()

app.include_router(user_route, prefix="/user")
app.include_router(event_route, prefix="/event")

settings = Settings()


@app.on_event("startup")
async def on_startup():
    await settings.initialize_database()


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")
