from typing import Optional
from pydantic import model_validator, BaseModel, ValidationError, Field


class SpaceStation(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    power: float = Field(ge=80, le=100)
    oxygen: float = Field(ge=80, le=100)
    crew: int = Field(ge=1, le=20)
    ID: str
    Last_maintenance: int
    Operational: bool = True
    Notes: Optional[str] = Field(max_length=200)

    @model_validator(mode="after")
    def validate_crew(self, value):
        print("==================================")
        print("Valid Space Program validated !")
        print("crew:", self.crew)
        print("Name:", self.name)
        print("ID:", self.ID)
        print(f"Energy: {self.power}%")
        print(f"Oxygen: {self.oxygen}%")
        print(f"Operational: {self.Operational}")
        print(f"Last Maintenance: {self.Last_maintenance}")
        print(f"Notes: {self.Notes}")
        print("\n==================================")
        return self


if __name__ == "__main__":
    try:
        SpaceStation(**{'crew': 20, 'name': "H.M.ISS", 'power': 90.0,
                     'oxygen': 100.0, 'ID': "HMI-SS-001", 'Operational': True},
                     Notes="From space to baka !", Last_maintenance=0)
        SpaceStation(**{'crew': "Funny", 'name': "H.M.ISS", 'power': 90.0,
                     'oxygen': 100.0, 'ID': "HMI-SS-001", 'Operational': True},
                     Notes="This should break.", Last_maintenance=600)
    except ValidationError as e:
        print("Invalid input:", e)
