from pydantic import BaseModel
from typing import List, Optional
from utils.player_mapper import PlayerMapper


class RosterSettings(BaseModel):
    wins: int
    waiver_position: int
    waiver_budget_used: int
    total_moves: int
    ties: int
    losses: int
    fpts: int
    fpts_decimal: Optional[int] = 0
    fpts_against_decimal: Optional[int] = 0
    fpts_against: Optional[int] = 0


class RosterResponse(BaseModel):
    starters: List[str]  # player IDs or team D/STs
    settings: RosterSettings
    roster_id: int
    reserve: Optional[List[str]]
    players: List[str]
    owner_id: str
    league_id: str

    def get_mapped_starters(self, mapper: "PlayerMapper") -> List[str]:
        return [mapper.map_players(pid) for pid in self.starters]

    def get_mapped_players(self, mapper: "PlayerMapper") -> List[str]:
        return [mapper.map_players(pid) for pid in self.players]

    def get_mapped_reserve(self, mapper: "PlayerMapper") -> List[str]:
        return [mapper.map_players(pid) for pid in self.reserve or []]
