from fastapi import FastAPI

from src.api.account import router as account
from src.api.image import router as image



app = FastAPI(debug=True)

app.include_router(account)
app.include_router(image)
