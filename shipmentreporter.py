import csv
import os
import sys
import sqlite3

from vessel import Vessel
from port import Port
from shipment import Shipment
from datetime import date


class Reporter:
    # How many vessels are there? -> int
    def total_amount_of_vessels(self) -> int:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM vessels"

        cursor.execute(query)
        amount_of_vessels = cursor.fetchone()[0]

        conn.close()
        return amount_of_vessels

    # What is the longest shipment distance? -> Shipment
    def longest_shipment(self) -> Shipment:
        conn = sqlite3.connect("shipments.db")
        cursor = conn.cursor()
        query = "SELECT * FROM shipments ORDER BY distance_naut DESC LIMIT 1"

        cursor.execute(query)
        longest_shipment = cursor.fetchone()

        print(longest_shipment)

        conn.close()
        return None

    # What is the longest and shortest vessel? -> tuple[Vessel, Vessel]
    def longest_and_shortest_vessels(self) -> tuple[Vessel, Vessel]:
        raise NotImplemented()

    # What is the widest and smallest vessel? -> tuple[Vessel, Vessel]
    def widest_and_smallest_vessels(self) -> tuple[Vessel, Vessel]:
        raise NotImplemented()

    # Which vessels have the most shipments -> tuple[Vessel, ...]
    def vessels_with_the_most_shipments(self) -> tuple[Vessel, ...]:
        raise NotImplemented()

    # Which ports have the most shipments -> tuple[Port, ...]
    def ports_with_most_shipments(self) -> tuple[Port, ...]:
        raise NotImplemented()

    # Which ports (origin) had the first shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the first shipment of a specific vessel type?  -> tuple[Port, ...]:
    def ports_with_first_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        raise NotImplemented()

    # Which ports (origin) had the latest shipment? -> tuple[Port, ...]:
    # Which ports (origin) had the latetst shipment of a specific vessel type? -> tuple[Port, ...]:
    def ports_with_latest_shipment(self, vessel_type: str = None) -> tuple[Port, ...]:
        raise NotImplemented()

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
        raise NotImplemented()

    # Which ports are located in country X? ->tuple[Port, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Ports in country X.csv`
    # example: `Ports in country Norway.csv`
    # otherwise it should just return the value as tuple(Port, ...)
    # CSV example (this are also the headers):
    #   id, code, name, city, province, country
    def ports_in_country(self, country: str, to_csv: bool = False) -> tuple[Port, ...]:
        raise NotImplemented()

    # Which vessels are from country X? -> tuple[Vessel, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Vessels from country X.csv`
    # example: `Vessels from country GER.csv`
    # otherwise it should just return the value as tuple(Vessel, ...)
    # CSV example (this are also the headers):
    #   imo, mmsi, name, country, type, build, gross, netto, length, beam
    def vessels_from_country(
        self, country: str, to_csv: bool = False
    ) -> tuple[Vessel, ...]:
        raise NotImplemented()


reporter = Reporter()

reporter.longest_shipment()
