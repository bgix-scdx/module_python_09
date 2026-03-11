from pydantic import model_validator, BaseModel, ValidationError, Field
from pydantic_core import PydanticCustomError
from typing import Optional
import enum


class ContactType(enum.Enum):
    VISUAL = "visual"
    AUDIO = "audio"
    RADIO = "radio"
    OTHER = "other"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: int
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str]
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact(self):
        if (self.contact_id[0] != 'A' or self.contact_id[1] != 'C'):
            raise ValidationError.from_exception_data(
                title="Invalid ID",
                line_errors=[{'type': PydanticCustomError("ID",
                              "ID need to start with AC"),
                              'input': self.contact_id}]
            )
        elif self.signal_strength < 7 and not self.message_received:
            raise ValidationError.from_exception_data(
                title="Invalid Strenght",
                line_errors=[{'type': PydanticCustomError("ID",
                              "Not enough strength for the signal"),
                              'input': self.signal_strength}]
            )
        else:
            print("======================================")
            print("Valid Contact Report: ")
            print(f"ID: {self.contact_id}")
            print(f"Type: {self.contact_type.value}")
            print(f"Location: {self.location}")
            print(f"Signal: {self.signal_strength}/10")
            print(f"Duration: {self.duration_minutes} minutes")
            print(f"Witness: {self.witness_count}")
            print(f"Message {self.message_received}")
            print("\n======================================")
            return self
        return self


try:
    AlienContact(contact_id="AC.67", timestamp=69696969,
                 location="Arecibo Observatory",
                 contact_type=ContactType.RADIO,
                 signal_strength=7.5, duration_minutes=345, witness_count=3,
                 message_received="Hello World!", is_verified=True)
    AlienContact(contact_id="AB.67", timestamp=69696969,
                 location="Arecibo Observatory",
                 contact_type=ContactType.RADIO,
                 signal_strength=7.5, duration_minutes=345, witness_count=10,
                 message_received="Hello World!", is_verified=True)
    AlienContact(contact_id=0, timestamp=69696969,
                 location="Arecibo Observatory",
                 contact_type=ContactType.RADIO,
                 signal_strength=7.5, duration_minutes=345, witness_count=3,
                 message_received="Hello World!", is_verified=True)
except ValidationError as e:
    print("ValidationError, class not validated.", e)
