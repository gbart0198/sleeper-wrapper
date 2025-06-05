from pydantic import BaseModel
from typing import Optional


class LeagueState(BaseModel):
    week: int
    season_type: str
    season_start_date: Optional[str]
    season: str
    previous_season: str
    leg: int
    league_season: str
    league_create_season: str
    display_week: int
