from pydantic import BaseModel


class UserResponse(BaseModel):
    username: str
    user_id: str
    display_name: str
    avatar: str
