from fastapi import FastAPI
from services import private

app = FastAPI()

app.include_router(private)


