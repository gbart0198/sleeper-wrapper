from typing import Optional, Dict
from pydantic import BaseModel


class LeagueUser(BaseModel):
    user_id: str
    display_name: str
    avatar: Optional[str]
    metadata: Optional[Dict[str, str]]
    is_owner: Optional[bool]
    is_bot: Optional[bool]
    league_id: str
