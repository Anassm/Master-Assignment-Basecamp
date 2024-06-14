from port import Port
from vessel import Vessel
import sqlite3
from datetime import date, timedelta


class Shipment:

    def __init__(
        self,
        id: str,
        date: date,  # ? Not sure if this type is correct
        cargo_weight: int,
        distance_naut: float,
        duration_hours: float,
        average_speed: float,
        origin: str,
        destination: str,
        vessel: int,
    ) -> None:
        self.id = id
        self.date = date
        self.cargo_weight = cargo_weight
        self.distance_naut = distance_naut
        self.duration_hours = duration_hours
        self.average_speed = average_speed
        self.origin = origin
        self.destination = destination
        self.vessel = vessel

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
    ):
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        shipment_query = "SELECT * FROM shipments WHERE id = ?"
        ports_query = "SELECT * FROM ports WHERE id = ?"
        cursor.execute(shipment_query, (self.id,))

        shipment_data = cursor.fetchone()

        cursor.execute(ports_query, (shipment_data[6],))
        origin = cursor.fetchone()

        cursor.execute(ports_query, (shipment_data[7],))
        destination = cursor.fetchone()

        ports = {
            "origin": Port(
                origin[0], origin[1], origin[2], origin[3], origin[4], origin[5]
            ),
            "destination": Port(
                destination[0],
                destination[1],
                destination[2],
                destination[3],
                destination[4],
                destination[5],
            ),
        }

        conn.close()
        return ports

    def get_vessel(self) -> Vessel:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        query = "SELECT * FROM vessels WHERE imo = ?"
        cursor.execute(query, (self.id,))
        vessel_data = cursor.fetchall()
        vessel_data = Vessel(
            vessel_data[0],
            vessel_data[1],
            vessel_data[2],
            vessel_data[3],
            vessel_data[4],
            vessel_data[5],
            vessel_data[6],
            vessel_data[7],
            vessel_data[8],
            vessel_data[9],
        )

        conn.close()
        return vessel_data

    def calculate_fuel_costs(self, price_per_liter: float, vessel: Vessel) -> float:
        fuel_consumption = vessel.get_fuel_consumption(self.distance_naut)
        fuel_costs = self.duration_hours * fuel_consumption * price_per_liter

        return round(fuel_costs, 3)

    def convert_speed(self, to_format: str) -> float:
        if to_format == "Knts":
            return round(self.average_speed, 6)
        elif to_format == "Mph":
            return round(self.average_speed * 1.15078, 6)
        elif to_format == "Kmph":
            return round(self.average_speed * 1.852, 6)
        else:
            raise ValueError

    def convert_distance(self, to_format: str) -> float:
        if to_format == "NM":
            return round(self.distance_naut, 6)
        elif to_format == "M":
            return round(self.distance_naut * 1852, 6)
        elif to_format == "KM":
            return round(self.distance_naut * 1.852, 6)
        elif to_format == "MI":
            return round(self.distance_naut * 1.15078, 6)
        elif to_format == "YD":
            return round(self.distance_naut * 2025.372, 6)
        else:
            raise ValueError("Invalid format")

    # Convert duration(to_format: str)(returns converted duration in the provided datetime format)
    # (example: %D%H will return days:hours, options are: %D = days, %H = hours, %M = minutes)

    def convert_duration(self, to_format: str) -> str:
        time = timedelta(hours=self.duration_hours)

        days = time.days
        hours = time.seconds // 3600 % 24
        minutes = (time.seconds // 60) % 60

        if to_format == "%D":
            return f"{days:02}"
        elif to_format == "%D:%H":
            return f"{days:02}:{hours:02}"
        elif to_format == "%D:%H:%M":
            return f"{days:02}:{hours:02}:{minutes:02}"
        elif to_format == "%H":
            return f"{hours:02}"
        elif to_format == "%H:%M":
            return f"{hours:02}:{minutes:02}"
        elif to_format == "%M":
            return f"{minutes:02}"
