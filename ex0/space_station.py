#!/usr/bin/env python3


from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):

    station_id: str = Field(..., min_length = 3, max_length = 10)
    name: str = Field(..., min_length = 1, max_length = 50)
    crew_size: int = Field(..., ge = 1, le = 20)
    power_level: float = Field(default = 100, ge = 0, le = 100)
    oxygen_level: float = Field(default = 100, ge = 0, le = 100)
    last_maintenance: datetime= Field(default = datetime.now())
    is_operational: bool = Field(default = True)
    notes: str = Field(default = "", max_length = 200)


def displaySpaceStaionInformation(spcst: SpaceStation) -> None:
    print(f"ID: {spcst.station_id}")
    print(f"Name: {spcst.name}")
    print(f"Crew: {spcst.crew_size} people")
    print(f"Power: {spcst.power_level}%")
    print(f"Oxygen: {spcst.oxygen_level}%")
    print(f"Status: {'NOT ' if not spcst.is_operational else ''}Operational")


def main() -> None:
    print("Space Station Data Validation")
    try:
        print("========================================")
        spaceStation = SpaceStation(
            station_id = "ISS001",
            name = "International Space Station",
            crew_size = 6,
            power_level = 85.5,
            oxygen_level = 92.3,
            last_maintenance = datetime.now(),
            is_operational = True,
            notes = "")
        print("Valid station created:")
        displaySpaceStaionInformation(spaceStation)
        print("")
        print("========================================")
        spaceStationErr = SpaceStation(
            station_id = "ISS002",
            name = "International Space Station 2",
            crew_size = 42)
        print("Valid station created:")
        displaySpaceStaionInformation(spaceStationErr)
        print("")
    except Exception as e:
        print("Expected validation error:")
        print(e)


if __name__ == "__main__":
    main()
