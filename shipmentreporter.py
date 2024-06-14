import csv
import sqlite3

from vessel import Vessel
from port import Port
from shipment import Shipment
from datetime import date
from collections import Counter


class Reporter:
    # How many vessels are there? -> int
    def total_amount_of_vessels(self) -> int:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM vessels"

        cursor.execute(query)
        amount_of_vessels = cursor.fetchone()[0]

        conn.close()
        return int(amount_of_vessels)

    # What is the longest shipment distance? -> Shipment
    def longest_shipment(self) -> Shipment:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = "SELECT * FROM shipments ORDER BY distance_naut DESC LIMIT 1"

        cursor.execute(query)
        longest_shipment = cursor.fetchone()

        conn.close()
        return Shipment(*longest_shipment)

    # What is the longest and shortest vessel? -> tuple[Vessel, Vessel]
    def longest_and_shortest_vessels(self) -> tuple[Vessel, Vessel]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query_longest = "SELECT * FROM vessels ORDER BY length DESC LIMIT 1"
        query_shortest = "SELECT * FROM vessels ORDER BY length ASC LIMIT 1"

        cursor.execute(query_longest)
        longest_vessel = cursor.fetchone()

        cursor.execute(query_shortest)
        shortest_vessel = cursor.fetchone()

        vessels = (Vessel(*longest_vessel), Vessel(*shortest_vessel))

        conn.close()
        return vessels

    # What is the widest and smallest vessel? -> tuple[Vessel, Vessel]
    def widest_and_smallest_vessels(self) -> tuple[Vessel, Vessel]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query_widest = "SELECT * FROM vessels ORDER BY beam DESC LIMIT 1"
        query_smallest = "SELECT * FROM vessels ORDER BY beam ASC LIMIT 1"

        cursor.execute(query_widest)
        widest_vessel = cursor.fetchone()

        cursor.execute(query_smallest)
        smallest_vessel = cursor.fetchone()

        vessels = (Vessel(*widest_vessel), Vessel(*smallest_vessel))

        conn.close()
        return vessels

    # Which vessels have the most shipments -> tuple[Vessel, ...]
    def vessels_with_the_most_shipments(self) -> tuple[Vessel, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = "SELECT vessel FROM shipments"

        cursor.execute(query)
        vessels = [vessel[0] for vessel in cursor.fetchall()]
        vessel_counter = Counter(vessels)
        most_used_vessel = vessel_counter.most_common(1)[0][0]

        query = "SELECT * FROM vessels WHERE imo = ?"
        cursor.execute(query, (most_used_vessel,))
        vessel = cursor.fetchone()

        conn.close()
        return (Vessel(*vessel),)

    # Which ports have the most shipments -> tuple[Port, ...]
    def ports_with_most_shipments(self) -> tuple[Port, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = (
            "SELECT origin FROM shipments UNION ALL SELECT destination FROM shipments"
        )

        cursor.execute(query)
        ports = [port[0] for port in cursor.fetchall()]
        port_counter = Counter(ports)
        most_used_port = port_counter.most_common(1)[0][0]

        query = "SELECT * FROM ports WHERE id = ?"
        cursor.execute(query, (most_used_port,))
        port = cursor.fetchone()

        conn.close()
        return (Port(*port),)

    # Which ports (origin) had the first shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the first shipment of a specific vessel type?  -> tuple[Port, ...]:

    def ports_with_first_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        if vessel_type is not None:
            query = "SELECT origin FROM shipments JOIN vessels ON shipments.vessel = vessels.imo WHERE vessels.type = ? ORDER BY date ASC"
            cursor.execute(
                query,
                (vessel_type,),
            )
            shipment = cursor.fetchone()

            query = "SELECT * FROM ports WHERE id = ?"
            cursor.execute(query, (shipment[0],))

            port = cursor.fetchone()
            return tuple(
                [
                    Port(
                        port[0],
                        port[1],
                        port[2],
                        port[3],
                        port[4],
                        port[5],
                    )
                ]
            )

        else:
            query = "SELECT * FROM shipments ORDER BY date ASC"
            cursor.execute(query)
            shipment = cursor.fetchall()

            shipment_list = []
            for ship in shipment:
                if ship[1] == shipment[0][1]:
                    shipment_list.append(ship)

            shipment_data = []
            shipment_list.sort(key=lambda x: x[6])

            query = "SELECT * FROM ports WHERE id = ?"
            for shipment in shipment_list:
                cursor.execute(query, (shipment[6],))
                port = cursor.fetchone()
                shipment_data.append(
                    Port(
                        port[0],
                        port[1],
                        port[2],
                        port[3],
                        port[4],
                        port[5],
                    )
                )

            return tuple(shipment_data)

    # Which ports (origin) had the latest shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the latetst shipment of a specific vessel type? -> tuple[Port, ...]:
    def ports_with_latest_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        if vessel_type is not None:
            query = "SELECT origin FROM shipments JOIN vessels ON shipments.vessel = vessels.imo WHERE vessels.type = ? ORDER BY date DESC"
            cursor.execute(
                query,
                (vessel_type,),
            )
            shipment = cursor.fetchone()

            query = "SELECT * FROM ports WHERE id = ?"
            cursor.execute(query, (shipment[0],))

            port = cursor.fetchone()
            return tuple(
                [
                    Port(
                        port[0],
                        port[1],
                        port[2],
                        port[3],
                        port[4],
                        port[5],
                    )
                ]
            )

        else:
            query = "SELECT * FROM shipments ORDER BY date DESC"
            cursor.execute(query)
            shipment = cursor.fetchall()

            shipment_list = []
            for ship in shipment:
                if ship[1] == shipment[0][1]:
                    shipment_list.append(ship)

            shipment_data = []
            shipment_list.sort(key=lambda x: x[6])

            query = "SELECT * FROM ports WHERE id = ?"
            for shipment in shipment_list:
                cursor.execute(query, (shipment[6],))
                port = cursor.fetchone()
                shipment_data.append(
                    Port(
                        port[0],
                        port[1],
                        port[2],
                        port[3],
                        port[4],
                        port[5],
                    )
                )

            return tuple(shipment_data)

    # Which vessels have docked port Z between period X and Y? -> tuple[Vessel, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Vessels docking Port Z between X and Y.csv`
    # example: `Vessels docking Port MZPOL between 2023-03-01 and 2023-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Vessels, ...)
    # CSV example (this are also the headers):
    #   imo, mmsi, name, country, type, build, gross, netto, length, beam
    def vessels_that_docked_port_between(
        self, port: Port, start: date, end: date, to_csv: bool = False
    ) -> tuple[Vessel, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        query = "SELECT vessel FROM shipments WHERE destination = ? AND date BETWEEN ? AND ? ORDER BY vessel ASC"
        cursor.execute(query, (port.id, start, end))
        shipments = [shipment[0] for shipment in cursor.fetchall()]

        query = "SELECT * FROM vessels WHERE imo = ?"
        vessels = []
        for shipment in shipments:
            cursor.execute(query, (shipment,))
            vessel = cursor.fetchone()
            vessels.append(
                Vessel(*vessel),
            )

        conn.close()

        if to_csv:
            start_date = start.strftime("%Y-%m-%d")
            end_date = end.strftime("%Y-%m-%d")

            with open(
                f"Vessels docking Port {port.id} between {start_date} and {end_date}.csv",
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "imo",
                        "mmsi",
                        "name",
                        "country",
                        "type",
                        "build",
                        "gross",
                        "netto",
                        "length",
                        "beam",
                    ]
                )
                for vessel in vessels:
                    writer.writerow(
                        [
                            vessel.imo,
                            vessel.mmsi,
                            vessel.name,
                            vessel.country,
                            vessel.type,
                            vessel.build,
                            vessel.gross,
                            vessel.netto,
                            vessel.length,
                            vessel.beam,
                        ]
                    )

        return tuple(vessels)

    # Which ports are located in country X? ->tuple[Port, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Ports in country X.csv`
    # example: `Ports in country Norway.csv`
    # otherwise it should just return the value as tuple(Port, ...)
    # CSV example (this are also the headers):
    #   id, code, name, city, province, country
    def ports_in_country(self, country: str, to_csv: bool = False) -> tuple[Port, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        query = "SELECT * FROM ports WHERE country = ? ORDER BY id ASC"
        cursor.execute(query, (country,))
        ports = cursor.fetchall()

        all_ports = []
        for port in ports:
            all_ports.append(
                Port(*port),
            )

        if to_csv:
            with open(f"Ports in country {country}.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "code", "name", "city", "province", "country"])
                for port in all_ports:
                    writer.writerow(
                        [
                            port.id,
                            port.code,
                            port.name,
                            port.city,
                            port.province,
                            port.country,
                        ]
                    )

        return tuple(all_ports)

    # Which vessels are from country X? -> tuple[Vessel, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Vessels from country X.csv`
    # example: `Vessels from country GER.csv`
    # otherwise it should just return the value as tuple(Vessel, ...)
    # CSV example (this are also the headers):
    #   imo, mmsi, name, country, type, build, gross, netto, length, beam
    def vessels_from_country(
        self, country: str, to_csv: bool = False
    ) -> tuple[Vessel, ...]:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()

        query = "SELECT * FROM vessels WHERE country = ? ORDER BY imo ASC"
        cursor.execute(query, (country,))
        vessels = cursor.fetchall()

        all_vessels = []
        for vessel in vessels:
            all_vessels.append(
                Vessel(*vessel),
            )

        if to_csv:
            with open(f"Vessels from country {country}.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "imo",
                        "mmsi",
                        "name",
                        "country",
                        "type",
                        "build",
                        "gross",
                        "netto",
                        "length",
                        "beam",
                    ]
                )
                for vessel in all_vessels:
                    writer.writerow(
                        [
                            vessel.imo,
                            vessel.mmsi,
                            vessel.name,
                            vessel.country,
                            vessel.type,
                            vessel.build,
                            vessel.gross,
                            vessel.netto,
                            vessel.length,
                            vessel.beam,
                        ]
                    )

        return tuple(all_vessels)


reporter = Reporter()

port = Port("CNTAO", 57047, "Qingdao", "Qingdao", "Shandong", "China")


# print(reporter.total_amount_of_vessels())
# print(reporter.longest_shipment())
# print(reporter.longest_and_shortest_vessels())
# print(reporter.widest_and_smallest_vessels())
# print(reporter.ports_with_first_shipment("Container Ship"))

# from datetime import datetime

# print(
#     reporter.vessels_that_docked_port_between(
#         port,
#         datetime.strptime("2023-03-01", "%Y-%m-%d").date(),
#         datetime.strptime("2024-06-01", "%Y-%m-%d").date(),
#         True,
#     )
# )

# print(reporter.ports_in_country("China"))
# print(reporter.vessels_from_country("Panama"))
