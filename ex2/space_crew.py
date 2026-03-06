from enum import Enum
from pydantic import model_validator, BaseModel, ValidationError, Field
from pydantic_core import PydanticCustomError
from typing import List


class Rank(Enum):
    cadet = "Cadet"
    officier = "Officier"
    lieutenant = "Lieutenant"
    captain = "Captain"
    commander = "Commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: int
    duration: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=3, max_length=12)
    mission_status: str = "planned"
    budget_million: float = Field(ge=1, le=10000)

    @model_validator(mode="after")
    def check(self) -> any:
        has_cap = False
        is_active = True
        experience_lvl = 0.0
        for crew in self.crew:
            if crew.rank == Rank.commander or crew.rank == Rank.captain:
                has_cap = True
            if crew.is_active is False:
                is_active = False
            experience_lvl += crew.years_experience / len(self.crew)
        if (self.mission_id[0] != "M"):
            raise ValidationError.from_exception_data(
                title="Invalid ID",
                line_errors=[{'type': PydanticCustomError("ID",
                              "ID need to start with M"),
                              'input': self.mission_id[0]}]
            )
        elif has_cap is False:
            raise ValidationError.from_exception_data(
                title="No leader",
                line_errors=[{'type': PydanticCustomError("crew",
                              "Need a commander or captain"),
                              'input': has_cap}]
            )
        elif self.duration > 365 and experience_lvl < 5.0:
            raise ValidationError.from_exception_data(
                title="Inexperienced Crew",
                line_errors=[{'type': PydanticCustomError("crew",
                              "No experience (<5)"),
                              'input': experience_lvl}]
            )
        elif is_active is False:
            raise ValidationError.from_exception_data(
                title="Inactive Crew",
                line_errors=[{'type': PydanticCustomError("crew", "Inactive"),
                              'input': is_active}]
            )
        return self

try:
    jef = CrewMember(member_id="JE01", name="JEFF", rank=Rank.captain, age=21,
                     specialization="Baka", years_experience=2, is_active=True)
    claude = CrewMember(member_id="JE01", name="JEFF", rank=Rank.cadet, age=24,
                     specialization="Cook", years_experience=6, is_active=True)
    SpaceMission(mission_id=".Space0", mission_name="Bakus Amogus",
                destination="Space", crew=[jef, claude], mission_status="Funny",
                budget_million=500.0, launch_date=25121221, duration=385)
except ValidationError as err:
    print(err)
