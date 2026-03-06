from pydantic import model_validator, BaseModel, ValidationError


class SpaceStation(BaseModel):
    name: str
    power: float
    oxygen: float
    crew: int
    ID: str
    Operational: bool = True

    @model_validator(mode="after")
    def validate_crew(self, value):
        if self.crew < 20:
            print("Not enought crew to start the program (minimim: 20)")
        elif len(self.name) > 50:
            print("Program name denied (maximum: 50)")
        elif len(self.name) < 3:
            print("Program name denied (maximum: 50)")
        elif self.power < 80:
            print("Not enought power to start the program (minimim: 80)")
        elif not self.Operational:
            print("Program not operational, please check the system.")
        else:
            print("==================================")
            print("Valid Space Program validated !")
            print("crew:", self.crew)
            print("Name:", self.name)
            print("ID:", self.ID)
            print(f"Energy: {self.power}%")
            print(f"Oxygen: {self.oxygen}%")
            print(f"Operational: {self.Operational}")
            print("\n==================================")
            return self
        return self


if __name__ == "__main__":
    try:
        SpaceStation(**{'crew': 26, 'name': "H.M.ISS", 'power': 90.0,
                     'oxygen': 100.0, 'ID': "HMI-SS-001", 'Operational': True})
        SpaceStation(**{'crew': "Funny", 'name': "H.M.ISS", 'power': 90.0,
                     'oxygen': 100.0, 'ID': "HMI-SS-001", 'Operational': True})
    except ValidationError as e:
        print("Invalid input:", e)
