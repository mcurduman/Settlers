import math
from typing import List, Tuple
from pydantic import BaseModel, Field
from engine.game.entities.resource_type import ResourceType


class HexTile(BaseModel):
    q: int = Field(..., description="Axial coordinate q")
    r: int = Field(..., description="Axial coordinate r")
    resource: ResourceType = Field(
        ..., description="Type of resource produced by this tile"
    )
    number: int | None = Field(
        default=None, description="Number token on the tile (None for desert)"
    )

    def center(self, size: float = 1.0) -> Tuple[float, float]:
        x = size * math.sqrt(3) * (self.q + self.r / 2)
        y = size * 1.5 * self.r
        return (x, y)

    def corners(self, size: float = 1.0) -> List[Tuple[float, float]]:
        cx, cy = self.center(size)
        corners = []

        for i in range(6):
            angle = math.radians(60 * i - 30)
            x = cx + size * math.cos(angle)
            y = cy + size * math.sin(angle)
            corners.append((x, y))

        return corners
