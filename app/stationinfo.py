"""
Contains StationInfo class. It is a containter to hold the information
for individual station. Data type enforced by pydantic.dataclasses.dataclass;

"""

from typing import Any, Tuple, Dict
from pydantic.dataclasses import dataclass


@dataclass
class StationInfo:
    """
    class for station information
    """

    station_id: str
    short_name: str
    full_name: str
    address: str
    coordinates: Tuple[float, float]
    total: int
    available: int
    occupied: int
    timestamp: str

    def annouce(self) -> str:
        """Return a string describing the station availability briefly

        Returns:
            str: _description_
        """
        return f"The station {self.short_name} has {self.available} available slots"

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the station info

        Returns:
            Dict[str, Any]: _description_
        """
        rlt_dict: Dict[str, Any] = self.__dict__
        del rlt_dict["__pydantic_initialised__"]
        return {self.station_id: rlt_dict}


def create_stationinfo_from_polars_row(row: tuple) -> StationInfo:
    """create a StationInfo instance from a polars row; The column
    location matters (no column name index)

    Args:
        row (tuple): polars row

    Returns:
        Self: StationInfo class
    """
    return StationInfo(
        station_id=row[0],
        short_name=row[3],
        full_name=row[2],
        address=row[4],
        coordinates=(row[5], row[6]),
        available=row[9],
        timestamp=row[10],
        total=row[7],
        occupied=row[8],
    )
