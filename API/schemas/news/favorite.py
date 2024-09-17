from pydantic import BaseModel
from typing import List, Optional

class FavoritesResponseSchema(BaseModel):
    user_id: int
    post_id: int