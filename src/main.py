from fastapi import FastAPI
from src.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
