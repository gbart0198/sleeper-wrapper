from pydantic import BaseModel
from typing import Optional, List, Dict, Literal, Union


class DraftPick(BaseModel):
    season: str
    round: int
    roster_id: int
    previous_owner_id: int
    owner_id: int


class WaiverBudgetTransaction(BaseModel):
    sender: int
    receiver: int
    amount: int


class LeagueTransactionResponse(BaseModel):
    type: Literal["trade", "waiver", "free_agent"]
    transaction_id: str
    status_updated: int
    status: Literal["complete", "failed", "pending"]
    settings: Optional[Dict[str, Union[int, str]]] = (
        None  # only applies for some waiver types
    )
    roster_ids: List[int]
    metadata: Optional[Dict[str, Union[str, int]]] = None
    leg: int
    drops: Optional[Dict[str, int]] = None  # player_id to roster_id
    adds: Optional[Dict[str, int]] = None  # player_id to roster_id
    draft_picks: List[DraftPick]
    creator: str  # user_id
    created: int
    consenter_ids: List[int]
    waiver_budget: List[WaiverBudgetTransaction]
