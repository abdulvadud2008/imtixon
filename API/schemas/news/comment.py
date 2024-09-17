from pydantic import BaseModel, Field

class CommentCreateSchema(BaseModel):
    post_id: int
    text: str = Field(max_length=48)


class CommentResponseSchema(BaseModel):
    user_id: int
    text: str
