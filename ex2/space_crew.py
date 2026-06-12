#!/usr/bin/env python3


from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime


class Rank(Enum):

    CADET = "cadet"
    OFFICIER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):

    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=False)


class SpaceMission(BaseModel):

    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(default=datetime.now())
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def missionIDMustStartWithM(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with \"M\"")
        return (self)

    @model_validator(mode='after')
    def mustHaveAtLeastOneCommanderOrCaptain(self) -> "SpaceMission":
        boss: bool = False
        for crew in self.crew:
            if crew.rank in [Rank.COMMANDER, Rank.CAPTAIN]:
                boss = True
        if not boss:
            raise ValueError("Mission must have at least one" +
                             " Commander or Captain")
        return (self)

    @model_validator(mode='after')
    def longMissionNeedExperiencedCrew(self) -> "SpaceMission":
        if self.duration_days > 365:
            experiencedCrew: int = 0
            for crew in self.crew:
                if crew.years_experience >= 5:
                    experiencedCrew += 1
            if experiencedCrew < len(self.crew) / 2:
                raise ValueError("Long missions (> 365 days) need 50%%" +
                                 " experienced crew (5+ years)")
        return (self)

    @model_validator(mode='after')
    def allCrewMembersMustBeActive(self) -> "SpaceMission":
        for crew in self.crew:
            if not crew.is_active:
                raise ValueError("All crew members must be active")
        return (self)


def displaySpaceMission(spcmss: SpaceMission) -> None:
    print(f"Mission: {spcmss.mission_name}")
    print(f"ID: {spcmss.mission_id}")
    print(f"Destination: {spcmss.destination}")
    print(f"Duration: {spcmss.duration_days} days")
    print(f"Budget: ${spcmss.budget_millions}M")
    print(f"Crew size: {len(spcmss.crew)}")
    print("Crew members:")
    for crew in spcmss.crew:
        print(f"- {crew.name} ({crew.rank.value}) - {crew.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    try:
        print("========================================")
        spaceMission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(member_id="001",
                           name="Sarah Connor",
                           rank=Rank.COMMANDER,
                           age=25,
                           specialization="Mission Command",
                           years_experience=2,
                           is_active=True),
                CrewMember(member_id="002",
                           name="John Smith",
                           rank=Rank.LIEUTENANT,
                           age=33,
                           specialization="Navigation",
                           years_experience=24,
                           is_active=True),
                CrewMember(member_id="003",
                           name="Alice Johnson",
                           rank=Rank.OFFICIER,
                           age=42,
                           specialization="Engineering",
                           years_experience=12,
                           is_active=True)
            ])
        print("Valid mission created:")
        displaySpaceMission(spaceMission)
        print("")
        print("========================================")
        spaceMission = SpaceMission(
            mission_id="M2027_JUPITER",
            mission_name="Jupiter trip",
            destination="Jupiter",
            duration_days=3210,
            budget_millions=9999.99,
            crew=[
                CrewMember(member_id="001",
                           name="Sarah Connor",
                           rank=Rank.CADET,
                           age=25,
                           specialization="Mission Command",
                           years_experience=2,
                           is_active=True),
                CrewMember(member_id="002",
                           name="John Smith",
                           rank=Rank.LIEUTENANT,
                           age=33,
                           specialization="Navigation",
                           years_experience=24,
                           is_active=True),
                CrewMember(member_id="003",
                           name="Alice Johnson",
                           rank=Rank.OFFICIER,
                           age=42,
                           specialization="Engineering",
                           years_experience=12,
                           is_active=True)
            ])
        print("Valid mission created:")
        displaySpaceMission(spaceMission)
        print("")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
