from fastapi import FastAPI

from src.api.auth import router as auth
from src.api.game.character import router as character



app = FastAPI(debug=True)

app.include_router(auth)
app.include_router(character)
