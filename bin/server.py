from fastapi import FastAPI

from src.api.account import router as account
from src.api.game.character import router as character



app = FastAPI(debug=True)

app.include_router(account)
app.include_router(character)
