from pydantic import model_validator, BaseModel, ValidationError
from typing import List, Dict, Optional


class AlienContact(BaseModel):
    contact_id: str