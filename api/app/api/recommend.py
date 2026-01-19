from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_recommendation():
    return {"message": "Recommendation"}

# post request received with body {userid: <user id value>} 
# fetch all the interactions of this user from the database, fetch all 5000 movies feature vectors
# interactions: [{id, userId, movieId, type, value, createdAt}, {...}, ...]
# multiply the movie vector of movies in each interaction with its corresponding interaction weight
# find resultant vector of these vectors   
# compute cosine similarity score of this resultant vector with each 5000 movie feature vector
# sort the score from most to least score
# create an array of movie ids from the sorted scores
# store it in the database
# return response 