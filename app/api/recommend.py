from fastapi import APIRouter, Depends
from pydantic import BaseModel
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
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

    # fetching interactions of the user and movie vectors
    query = f'SELECT * FROM "UserInteractionMovies" where "userId" = \'{userId}\''
    interactions_df = pd.read_sql(query, engine)
    interactions = interactions_df.to_dict(orient="records")

    movie_feature_vectors = sparse.load_npz("data/movie_feature_vectors.npz")
    movie_ids = np.load("data/movie_ids.npy")

    # dict for mapping movie id to movie index in the feature vector
    movie_id_to_index = {
        movie_id: idx for idx, movie_id in enumerate(movie_ids)
    }

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

        idx = movie_id_to_index.get(movie_id)
        # remove the interaction if movie does not have a vector
        if idx is None: 
            continue

        if movie_id not in best_interaction_per_movie:
            best_interaction_per_movie[movie_id] = interaction
        else:
            if priority[interaction["type"]] > priority[best_interaction_per_movie[movie_id]["type"]]:
                best_interaction_per_movie[movie_id] = interaction    

    # keep top 50 most recently interacted movies
    sorted_interactions = sorted(
        best_interaction_per_movie.values(),
        key=lambda x: x["createdAt"],
        reverse=True
    )
    best_interactions = sorted_interactions[:50]

    # defining weight for each kind of interaction
    base_weights = {
        "RATED": 2.5,
        "WATCHLIST": 1.0,
        "SEARCH": 0.5,
        "CLICK": 0.25
    }

    def interaction_weight(interaction):
        if interaction["type"] == "RATED":
            return base_weights["RATED"] * (interaction["value"] / 10)
        return base_weights.get(interaction["type"])

    # creating the user vector
    user_vector = None
    total_weight = 0.0

    for interaction in best_interactions:  
        movie_id = interaction["movieId"]
        idx = movie_id_to_index.get(movie_id)

        weight = interaction_weight(interaction)
        if weight == 0:
            continue

        movie_vector = movie_feature_vectors[idx] * weight

        if user_vector is None:
            user_vector = movie_vector
        else:
            user_vector += movie_vector

        total_weight += weight

    if user_vector is not None and total_weight > 0:
        user_vector = user_vector / total_weight

    # compute cosine similarity and get top 2000 most similar movies
    similarities = cosine_similarity(user_vector, movie_feature_vectors)

    top_n = 2000
    top_indices = np.argsort(similarities[0])[::-1][:top_n]  
    top_movie_ids = movie_ids[top_indices]

    # return the recommendation array
    recommendation_list = top_movie_ids.tolist()
    
    return {
        "userId": userId,
        "recommendations": recommendation_list 
    }