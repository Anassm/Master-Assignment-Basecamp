from datetime import datetime as d
from port import Port
from vessel import Vessel


class Shipment:

    def __init__(
        self,
        id: str,
        date: d.date,  # ? Not sure if this type is correct
        cargo_weight: int,
        distance_naut: float,
        duration_hours: float,
        average_speed: float,
        origin: str,
        destination: str,
        vessel: int,
    ) -> None:
        pass

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]),
        )

    def get_ports(
        self,
    ) -> {
        "origin": Port,
        "destination": Port,
    }: ...  # ? Double check if expected output is correct

    def get_vessel(self) -> Vessel: ...

    def calculate_fuel_costs(self, price_per_liter: float, vessel: Vessel) -> float: ...

    def convert_speed(self, to_format: str) -> float: ...

    def convert_distance(self, to_format: str) -> float: ...

    def convert_duration(self, to_format: str) -> str: ...
