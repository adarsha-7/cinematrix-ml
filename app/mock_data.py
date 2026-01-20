import pandas as pd
from datetime import datetime
import uuid

# Mock data
interactions = [
    # Ratings
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 27205, "type": "RATED", "value": 7, "createdAt": datetime.now()},
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 157336, "type": "RATED", "value": 8, "createdAt": datetime.now()},
    
    # Watchlist
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 155, "type": "WATCHLIST", "value": None, "createdAt": datetime.now()},
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 19995, "type": "WATCHLIST", "value": None, "createdAt": datetime.now()},
    
    # Search
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 24428, "type": "SEARCH", "value": None, "createdAt": datetime.now()},
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 293660, "type": "SEARCH", "value": None, "createdAt": datetime.now()},
    
    # Clicks
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 299536, "type": "CLICK", "value": None, "createdAt": datetime.now()},
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 27205, "type": "CLICK", "value": None, "createdAt": datetime.now()},
    {"id": str(uuid.uuid4()), "userId": "hWj38qY2YNPxqFyJZLjT2C8CJtRmRgb2", "movieId": 157336, "type": "CLICK", "value": None, "createdAt": datetime.now()},
]

interactions_df = pd.DataFrame(interactions)


