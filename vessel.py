import sqlite3


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
        self.imo = imo
        self.mmsi = mmsi
        self.name = name
        self.country = country
        self.type = type
        self.build = build
        self.gross = gross
        self.netto = netto
        self.length = length
        self.beam = beam

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]),
        )

    def get_fuel_consumption(self, distance: float) -> float:
        ship_types = {
                        'Aggregates Carrier': 0.4,
                        'Bulk Carrier': 0.35,
                        'Bulk/Oil Carrier': 0.35,
                        'Cement Carrier': 0.4,
                        'Container Ship': 0.3,
                        'Deck Cargo Ship': 0.4,
                        'General Cargo Ship': 0.4,
                        'Heavy Load Carrier': 0.4,
                        'Landing Craft': 0.4,
                        'Nuclear Fuel Carrier': 0.35,
                        'Palletised Cargo Ship': 0.4,
                        'Passenger/Container Ship': 0.3,
                        'Ro-Ro Cargo Ship': 0.4,
                        'Self Discharging Bulk Carrier': 0.35,
                        'Vehicles Carrier': 0.35,
                        'Wood Chips Carrier': 0.4
                      }
        if self.type in ship_types:
            efficiency = ship_types[self.type]
            
        consumption = efficiency * (self.gross / self.netto) * distance
        
        return round(consumption, 5)

    # Return float number based on the calculations from master assignment pdf

    # ? Ask teacher if it needs to return a tuple or a list -> onduidelijkheid van docent, zegt dat het niet uitmaakt.
    def get_shipments(
        self,
    ) -> tuple():  # ? Does Shipment need to be expected in output too?
        from shipment import Shipment

        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        get_query = "SELECT * FROM shipments WHERE vessel = ?"

        cursor.execute(get_query, (self.imo,))
        shipments = cursor.fetchall()

        all_shipments = []
        for shipment in shipments:
            all_shipments.append(
                Shipment(
                    shipment[0],
                    shipment[1],
                    shipment[2],
                    shipment[3],
                    shipment[4],
                    shipment[5],
                    shipment[6],
                    shipment[7],
                    shipment[8],
                )
            )

        conn.close()

        return tuple(all_shipments)