from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import recommend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", 
                   "https://cinematrix.adarshaghimire.com.np"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])

@app.head("/")
async def root():
    return {"message": "Welcome to Cinematrix movie recommendation API."}

@app.get("/")
async def root():
    return {"message": "Welcome to Cinematrix movie recommendation API."}