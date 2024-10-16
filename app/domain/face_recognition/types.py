from typing import Annotated, List

from pydantic import Field


FaceEncoding = Annotated[List[float], Field(min_length=128, max_length=128)]
