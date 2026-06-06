#!/usr/bin/env python3


from pydantic import BaseModel, Field, model_validator
from datetime import datetime


class AlienContact(BaseModel):

    contact_id: str = Field(..., min_length = 5, max_length = 15)
    timestamp: datetime= Field(default = datetime.now())
    location: str = Field(..., min_length = 3, max_length = 100)
    contact_type: str = Field(..., values=["radio", "visual", "physical", "telepathic"])
    signal_strength: float = Field(default = 0, ge = 0, le = 10)
    duration_minutes: int = Field(..., ge = 1, le = 1440)
    witness_count: int = Field(..., ge = 1, le = 100)
    message_received: str = Field(default = "", max_length = 500)
    is_verified: bool = Field(default = False)

    @model_validator(mode='after')
    def contactIDMustStartWithAC(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with \"AC\" (Alien Contact)")
        return (self)

    @model_validator(mode='after')
    def physicalContactReportMustBeVerified(self) -> "AlienContact":
        if self.contact_type == "physical" and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        return (self)

    @model_validator(mode='after')
    def telepathicContactRequiresAtLeast3Witnesses(self) -> "AlienContact":
        if self.contact_type == "telepathic" and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")
        return (self)

    @model_validator(mode='after')
    def strongSignalShouldIncludeReceivedMessages(self) -> "AlienContact":
        if self.signal_strength > 7 and self.message_received == "":
            raise ValueError("Strong signals (> 7.0) should include received messages")
        return (self)


def displayAlienContact(ac: AlienContact) -> None:
    print(f"ID: {ac.contact_id}")
    print(f"Type: {ac.contact_type}")
    print(f"Location: {ac.location}")
    print(f"Signal: {ac.signal_strength}/10")
    print(f"Duration: {ac.duration_minutes} minutes")
    print(f"Witnesses: {ac.witness_count}")
    print(f"Message: '{ac.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    try:
        print("========================================")
        alienContact = AlienContact(
            contact_id = "AC_2024_001",
            contact_type = "radio",
            location = "Area 51, Nevada",
            signal_strength = 8.5,
            duration_minutes = 45,
            witness_count = 5,
            message_received = "Greetings from Zeta Reticuli")
        print("Valid contact report:")
        displayAlienContact(alienContact)
        print("")
        print("========================================")
        alienContactErr = AlienContact(
            contact_id = "AC2025_05",
            location = "International Space Station 2",
            contact_type = "telepathic",
            signal_strength = 8,
            duration_minutes = 42,
            witness_count = 6)
        print("Valid station created:")
        displayAlienContact(alienContactErr)
        print("")
        print("========================================")
        alienContact3 = AlienContact(
            contact_id = "AC_2024_003",
            contact_type = "physical",
            location = "Area 51, Nevada",
            signal_strength = 10,
            duration_minutes = 12,
            witness_count = 8,
            message_received = "Hi, don't panic !!!")
        print("Valid contact report:")
        displayAlienContact(alienContact3)
        print("")
    except Exception as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
