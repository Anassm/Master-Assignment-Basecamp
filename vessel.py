from shipment import Shipment


class Vessel:

    def __init__(
        self,
        imo: int,
        mmsi: int,
        name: str,
        country: str,
        type: str,
        build: int,
        gross: int,
        netto: int,
        length: int,
        beam: int,
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

    def get_fuel_consumption(self, distance: float) -> float: ...

    # Return float number based on the calculations from master assignment pdf

    # ? Ask teacher if it needs to return a tuple or a list -> onduidelijkheid van docent, zegt dat het niet uitmaakt.
    def get_shipments(self) -> list(Shipments): ...
