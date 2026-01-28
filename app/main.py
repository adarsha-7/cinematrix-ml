from fastapi import FastAPI
from api import recommend

app = FastAPI()

app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])

@app.head("/")
async def root():
    return {"message": "Welcome to Cinematrix movie recommendation API."}

@app.get("/")
async def root():
    return {"message": "Welcome to Cinematrix movie recommendation API."}