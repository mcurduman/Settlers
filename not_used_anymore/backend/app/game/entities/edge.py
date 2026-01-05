from typing import Optional, Tuple
from pydantic import BaseModel, Field


class Edge(BaseModel):
    a: Tuple[float, float] = Field(
        ..., description="Pixel coordinates of the first endpoint of the edge"
    )
    b: Tuple[float, float] = Field(
        ..., description="Pixel coordinates of the second endpoint of the edge"
    )
    owner: Optional[str] = Field(
        default=None, description="Player name who owns the road"
    )
