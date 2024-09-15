from pydantic import BaseModel

class FavoritesResponseSchema(BaseModel):
    user_id: int
    post_id: int

    class Config:
        from_attributes=True