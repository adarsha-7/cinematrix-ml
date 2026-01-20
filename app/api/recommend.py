from fastapi import APIRouter, Depends
from pydantic import BaseModel
import pandas as pd
import io
from scipy import sparse
from core.security import verify_api_key
from db import engine

# temporary import
from mock_data import interactions_df

router = APIRouter()

class X(BaseModel):
    userId: int

@router.get("/")
async def get_recommendation():
    return {"message": "movie recommendation route"}

@router.post("/", dependencies=[Depends(verify_api_key)])
async def get_recommendation(X: X):
    userId = X.userId

    # fetching interactions of the user
    interactions = interactions_df.to_dict(orient="records")
    
    # loading all movies sparse vector
    query = 'SELECT "combinedVector" FROM "MovieFeatureVector"'
    movie_feature_vectors_df = pd.read_sql(query, engine)
    sparse_vectors = [
        sparse.load_npz(io.BytesIO(b))
        for b in movie_feature_vectors_df["combinedVector"]
        if b is not None
    ]
    movie_feature_vectors = sparse.vstack(sparse_vectors)

    return {
        "message": f"this is the userId: {userId}"
    }

# DONE post request received with body {userid: <user id value>} 
# fetch all the interactions of this user from the database, load all 5000 movies sparse vectors
# interactions: [{id, userId, movieId, type, value, createdAt}, {...}, ...]
# multiply the movie vector of movies in each interaction with its corresponding interaction weight
# find resultant vector of these vectors   
# compute cosine similarity score of this resultant vector with each 5000 movie feature vector
# sort the score from most to least score
# create an array of movie ids from the sorted scores
# store it in the database
# return response 