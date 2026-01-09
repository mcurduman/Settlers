from typing import Optional, Tuple

from pydantic import BaseModel, Field


class Node(BaseModel):
    position: Tuple[float, float] = Field(
        ..., description="Pixel coordinates of the node"
    )
    owner: Optional[str] = Field(
        default=None, description="Player name who owns the settlement/city"
    )
