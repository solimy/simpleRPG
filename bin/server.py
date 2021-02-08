from fastapi import FastAPI

from src.api.auth import router as auth



app = FastAPI(debug=True)

app.include_router(auth)
