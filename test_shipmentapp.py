from vessel import Vessel
from shipment import Shipment
from port import Port


# Test to check if duration is converted correctly based on the given arguments
# 1) %D:%H:%M
# 2) %H:%M
def test_convert_duration():
    raise NotImplemented()


# Test to check if distance is converted correctly based on the given arguments
# 1) NM = Nautical Meters
# 2) M = Meters
# 3) KM = Kilometers
# 4) MI = Miles
# 5) YD = Yards
# 6) ValueError check
def test_convert_distance():
    raise NotImplemented()


# Test to check if speed is converted correctly based on the given arguments
# 1) Knts = Knots
# 2) Mph = Miles per hour
# 3) Kph = Kilometers per hour
# 4) ValueError check
def test_convert_speed():
    raise NotImplemented()


# Test to check if the fuel consumption is calculated correctly based on the distance
def test_get_fuel_consupmtion():
    raise NotImplemented()


# Test to check if the fuel costs are calculated correctly based on the price per liter
def test_calculate_fuel_costs():
    raise NotImplemented()


# Test to check if the returned ports are correct
# 1) amount check
# 2) keys check
# 3) values check
def test_get_ports():
    raise NotImplemented()


# Test if the returned shipments contain the required shipment(s)
def test_get_shipments_port():
    port = Port("NZWLG", 61447, "Wellington" "Wellington" "Wellington" "New Zealand")

    assert str(port.get_shipments()) == str(
        (
            Shipment(
                "92204C50-AF15-4228-8B46-AD73D2A9FBBF",
                "14-04-2023",
                42659,
                10581.898,
                1410.92,
                7.5,
                "USCLE",
                "NZWLG",
                9863833,
            ),
            Shipment(
                "A2C45241-2A55-4182-B7A7-83D39C98CE24",
                "28-06-2023",
                47401,
                5946.902,
                874.544,
                6.8,
                "NZWLG",
                "CLPTI",
                9863833,
            ),
        )
    )


def test_get_shipments_vessel():
    vessel = Vessel(
        1034034,
        None,
        "GREAT WALL 17",
        "Tanzania",
        "Deck Cargo Ship",
        2023,
        1978,
        2373,
        84,
        19,
    )

    assert str(vessel.get_shipments()) == str(
        (
            Shipment(
                "C8046337-CDC8-4A61-AD2E-8A12CA687C3C",
                "01-01-2024",
                1704,
                4120.326,
                251.239,
                16.4,
                "CNJMN",
                "INJDH",
                1034034,
            ),
            Shipment(
                "0E9E346C-623E-4FB2-9558-1F234E418485",
                "01-11-2023",
                1193,
                8451.304,
                361.167,
                23.4,
                "CNTAG",
                "UAKHE",
                1034034,
            ),
            Shipment(
                "8FD044E8-E3A5-45CC-B7A4-5F571FC41F4C",
                "26-11-2023",
                1605,
                7708.562,
                443.021,
                17.4,
                "UAKHE",
                "CNJMN",
                1034034,
            ),
        )
    )
