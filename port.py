import sqlite3


class Port:

    def __init__(
        self, id: str, code: int, name: str, city: str, province: str, country: str
    ) -> None:

        self.id = id
        self.code = code
        self.name = name
        self.city = city
        self.province = province
        self.country = country

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]),
        )

    def get_shipments(
        self,
    ) -> tuple():  # ? Does Shipment need to be expected in output too?
        from shipment import Shipment

        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        get_query = "SELECT * FROM shipments WHERE origin = ? OR destination = ?"

        cursor.execute(get_query, (self.id, self.id))
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
