from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class StatusDetailsDTO(BaseModel):
    status: str
    borrower_id: Optional[int] = Field(alias="borrowerId", default=None)
    borrower_name: Optional[str] = Field(alias="borrowerName", default=None)
    borrowed_on: Optional[datetime] = Field(alias="borrowedOn", default=None)

    model_config = ConfigDict(
        from_attributes=True,      # allow .from_orm()
        populate_by_name=True      # accept/emit camelCase aliases in JSON
    )