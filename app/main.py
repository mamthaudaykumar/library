# app/main.py
from fastapi import FastAPI

from app.controller import book_controller
from app.repository.seed_data import run_seed
from controller import user_wishlist_controller

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    run_seed()

app.include_router(book_controller.router)
app.include_router(user_wishlist_controller.router)



@app.get("/")
def health():
    return {"Hello": "Am up please see the documentation for usage"}
