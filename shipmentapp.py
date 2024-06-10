import os
import sys
import json
import sqlite3

# from vessel import Vessel
# from port import Port
# from shipment import Shipment


def get_json_data(file_path: str) -> list:
    with open(file_path, "r") as file:

        return json.load(file)


def fill_database(data: list):
    conn = sqlite3.connect("shipments.db")
    cursor = conn.cursor()

    # Fill Shipment table
    shipment_insert_query = "INSERT INTO shipments (id, date, cargo_weight, distance_naut, duration_hours, average_speed, origin, destination, vessel) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    shipment_insert_data = [
        (
            shipment["tracking_number"],
            shipment["date"],
            shipment["cargo_weight"],
            shipment["distance_naut"],
            shipment["duration_hours"],
            shipment["average_speed"],
            shipment["origin"],
            shipment["destination"],
            shipment["vessel"],
        )
        for shipment in data
    ]

    # Fill Vessel table
    vessel_insert_query = "INSERT INTO vessels (imo, mmsi, name, country, type, build, gross, netto, length, beam) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    vessel_insert_data = [
        (
            shipment["vessel"]["imo"],
            shipment["vessel"]["mmsi"],
            shipment["vessel"]["name"],
            shipment["vessel"]["country"],
            shipment["vessel"]["type"],
            shipment["vessel"]["build"],
            shipment["vessel"]["gross"],
            shipment["vessel"]["netto"],
            shipment["vessel"]["size"].split(" / ")[0],
            shipment["vessel"]["size"].split(" / ")[1],
        )
        for shipment in data
    ]

    # Fill Port table
    port_insert_query = "INSERT INTO ports (id, code, name, city, province, country) VALUES (?, ?, ?, ?, ?, ?)"
    port_insert_data = [
        (
            port["id"],
            port["code"],
            port["name"],
            port["city"],
            port["province"],
            port["country"],
        )
        for port in {shipment["origin"] for shipment in data}.union(
            {shipment["destination"] for shipment in data}
        )
    ]

    cursor.executemany(shipment_insert_query, shipment_insert_data)
    cursor.executemany(vessel_insert_query, vessel_insert_data)
    
    # TODO: apart loopen
    # Execute origin
    cursor.executemany(port_insert_query, port_insert_data)
    # Execute destination
    cursor.executemany(port_insert_query, port_insert_data)

    conn.commit()
    conn.close()


def main():
    data = get_json_data(os.path.join(sys.path[0], "shipments.json"))

    fill_database(data)


if __name__ == "__main__":
    main()
