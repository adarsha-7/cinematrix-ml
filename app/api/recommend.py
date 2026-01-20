from fastapi import APIRouter, Depends
from pydantic import BaseModel
import pandas as pd
import numpy as np
from scipy import sparse
from core.security import verify_api_key
from db.engine import engine

router = APIRouter()

class X(BaseModel):
    userId: str

@router.get("/")
async def get_recommendation():
    return {"message": "movie recommendation route"}

@router.post("/", dependencies=[Depends(verify_api_key)])
async def get_recommendation(X: X):
    userId = X.userId

    # fetching interactions of the user
    query = f'SELECT * FROM "UserInteractionMovies" where "userId" = \'{userId}\''
    interactions_df = pd.read_sql(query, engine)
    interactions = interactions_df.to_dict(orient="records")

    # defining weight for each kind of interaction
    def interaction_weight(interaction):
        if interaction["type"] == "RATED":
            return 2.5 * (interaction["value"] / 10)
        if interaction["type"] == "WATCHLIST":
            return 1.0
        if interaction["type"] == "SEARCH": 
            return 0.5
        if interaction["type"] == "CLICK": 
            return 0.25
        return 0.0

    # keeping the most important interaction for each movie
    priority = {
        "RATED": 4,
        "WATCHLIST": 3,
        "SEARCH": 2,
        "CLICK": 1
    }

    best_interaction_per_movie = {}

    for interaction in interactions:
        movie_id = interaction["movieId"]

        if movie_id not in best_interaction_per_movie:
            best_interaction_per_movie[movie_id] = interaction
        else:
            if priority[interaction["type"]] > priority[best_interaction_per_movie[movie_id]["type"]]:
                best_interaction_per_movie[movie_id] = interaction

    sorted_interactions = sorted(
        best_interaction_per_movie.values(),
        key=lambda x: x["createdAt"],
        reverse=True
    )

    # Keep top 50 most recently interacted movies
    best_interaction_per_movie = sorted_interactions[:50]

    # loading movie feature vectors
    movie_feature_vectors = sparse.load_npz("data/movie_feature_vectors.npz")
    movie_ids = np.load("data/movie_ids.npy")

    movie_id_to_index = {
        movie_id: idx for idx, movie_id in enumerate(movie_ids)
    }

    # creating final user vector
    user_vector = None
    total_weight = 0.0

    for movie_id, interaction in best_interaction_per_movie.items():
        idx = movie_id_to_index.get(movie_id)
        if idx is None:
            continue

        weight = interaction_weight(interaction)
        if weight == 0:
            continue

        movie_vector = movie_feature_vectors[idx] * weight

        user_vector = (movie_vector if user_vector is None else user_vector + movie_vector)
        total_weight += weight

    if user_vector is not None and total_weight > 0:
        user_vector = user_vector / total_weight

    return {
        "message": f"this is the userId: {userId}"
    }

# compute cosine similarity score of this resultant vector with each 5000 movie feature vector
# sort the score from most to least score
# create an array of movie ids from the sorted scores
# store it in the database
# return response 