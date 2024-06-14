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
            shipment["origin"]["id"],
            shipment["destination"]["id"],
            shipment["vessel"]["imo"],
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
    vessel_insert_data = list(set(vessel_insert_data))

    # Fill Port table with origin
    port_insert_query = "INSERT INTO ports (id, code, name, city, province, country) VALUES (?, ?, ?, ?, ?, ?)"
    port_insert_origin_data = [
        (
            port["id"],
            port["code"],
            port["name"],
            port["city"],
            port["province"],
            port["country"],
        )
        for port in (shipment["origin"] for shipment in data)
    ]
    port_insert_origin_data = list(set(port_insert_origin_data))

    # Fill Port table with destination
    port_insert_destination_data = [
        (
            port["id"],
            port["code"],
            port["name"],
            port["city"],
            port["province"],
            port["country"],
        )
        for port in (shipment["destination"] for shipment in data)
    ]
    port_total_data = port_insert_origin_data + port_insert_destination_data
    port_total_data = list(set(port_total_data))

    # Delete all data from tables for fresh start
    cursor.execute("DELETE FROM shipments")
    cursor.execute("DELETE FROM vessels")
    cursor.execute("DELETE FROM ports")

    cursor.executemany(shipment_insert_query, shipment_insert_data)
    cursor.executemany(vessel_insert_query, vessel_insert_data)
    cursor.executemany(port_insert_query, port_total_data)

    conn.commit()
    conn.close()


def main():
    json_data = get_json_data(os.path.join(sys.path[0], "shipments.json"))

    fill_database(json_data)


if __name__ == "__main__":
    main()
