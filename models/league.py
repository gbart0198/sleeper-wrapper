from typing import Any, List, Optional
from pydantic import BaseModel


class LeagueResponse(BaseModel):
    total_rosters: int
    status: str  # e.g. "pre_draft", "drafting", "in_season", or "complete"
    sport: str
    settings: Any
    season_type: str
    season: str
    scoring_settings: Any
    roster_positions: List[Any]
    previous_league_id: Optional[str]
    name: str
    league_id: str
    draft_id: str
    avatar: Optional[str]
