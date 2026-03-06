from pydantic import model_validator, BaseModel, ValidationError, Field
from typing import Optional
import enum


class ContactType(enum.Enum):
    VISUAL = "visual"
    AUDIO = "audio"
    RADIO = "radio"
    OTHER = "other"


class AlienContact(BaseModel):
    contact_id: str
    timestamp: int
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float
    duration_minutes: int
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str]
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact(self):
        if (
             len(self.contact_id) < 5 or len(self.contact_id) > 15
             and self.contact_id[0] != 'A' or self.contact_id[1] != 'C'):
            print("Invalid contact ID")
        elif self.duration_minutes / 60 >= 24:
            print("Duration cannot exceed 24 hours.")
        elif self.signal_strength < 7 and not self.message_received:
            print("Signal could not be recieved")
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
    AlienContact(contact_id="AC.67", timestamp=69696969,
                 location="Arecibo Observatory",
                 contact_type=ContactType.RADIO,
                 signal_strength=7.5, duration_minutes=345, witness_count=0,
                 message_received="Hello World!", is_verified=True)
    AlienContact(contact_id=0, timestamp=69696969,
                 location="Arecibo Observatory",
                 contact_type=ContactType.RADIO,
                 signal_strength=7.5, duration_minutes=345, witness_count=3,
                 message_received="Hello World!", is_verified=True)
except ValidationError:
    print("ValidationError, class not validated.")
