from vessel import Vessel
from shipment import Shipment
from port import Port
from datetime import timedelta


# Test to check if duration is converted correctly based on the given arguments
# 1) %D:%H:%M
# 2) %H:%M
def test_convert_duration():
    shipment = Shipment(
        "78067E7F-D833-4312-A805-C1355F51F065",
        "01-01-2023",
        15649,
        5879.249,
        864.595,
        6.8,
        "MYTPP",
        "TRGEM",
        9913547,
    )
    
    time = timedelta(hours=864.595)
    
    days = time.days
    hours = time.seconds // 3600
    minutes = (time.seconds // 60) % 60
    
    assert shipment.convert_duration("%D:%H:%M") == f"{days:02}:{hours:02}:{minutes:02}"
    assert shipment.convert_duration("%H:%M") == f"{hours:02}:{minutes:02}"

# Test to check if distance is converted correctly based on the given arguments
# 1) NM = Nautical Meters
# 2) M = Meters
# 3) KM = Kilometers
# 4) MI = Miles
# 5) YD = Yards
# 6) ValueError check
def test_convert_distance():
    shipment = Shipment(
        "78067E7F-D833-4312-A805-C1355F51F065",
        "01-01-2023",
        15649,
        5879.249,
        864.595,
        6.8,
        "MYTPP",
        "TRGEM",
        9913547,
    )
    
    assert shipment.convert_distance("NM") == round(5879.249, 6)
    assert shipment.convert_distance("M") == round(5879.249 * 1852, 6)
    assert shipment.convert_distance("KM") == round(5879.249 * 1.852, 6)
    assert shipment.convert_distance("MI") == round(5879.249 * 1.15078, 6)
    assert shipment.convert_distance("YD") == round(5879.249 * 2025.372, 6)
    assert shipment.convert_distance("CM") == ValueError
    


# Test to check if speed is converted correctly based on the given arguments
# 1) Knts = Knots
# 2) Mph = Miles per hour
# 3) Kph = Kilometers per hour
# 4) ValueError check
def test_convert_speed():
    shipment = Shipment(
        "78067E7F-D833-4312-A805-C1355F51F065",
        "01-01-2023",
        15649,
        5879.249,
        864.595,
        6.8,
        "MYTPP",
        "TRGEM",
        9913547,
    )
    
    assert shipment.convert_speed("Knts") == round(6.8, 6)
    assert shipment.convert_speed("Mph") == round(6.8 * 1.15078, 6)
    assert shipment.convert_speed("Kmph") == round(6.8 * 1.852, 6)
    assert shipment.convert_speed("Bpm") == ValueError


# Test to check if the fuel consumption is calculated correctly based on the distance
def test_get_fuel_consupmtion():
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

    assert vessel.get_fuel_consumption(4120.326) == round(0.4 * (1978 / 2373) * 4120.326, 5)


# Test to check if the fuel costs are calculated correctly based on the price per liter
def test_calculate_fuel_costs():
    shipment = Shipment(
        "78067E7F-D833-4312-A805-C1355F51F065",
        "01-01-2023",
        15649,
        5879.249,
        864.595,
        6.8,
        "MYTPP",
        "TRGEM",
        9913547,
    )
    vessel = Vessel(
        9913547,
        477736400,
        "TIGER LONGKOU",
        "Hong Kong",
        "Deck Cargo Ship",
        2022,
        23040,
        26200,
        192,
        37,
    )
    
    fuel_consumption = vessel.get_fuel_consumption(5879.249)
    assert shipment.calculate_fuel_costs(4.5, vessel) == round(864.595 * fuel_consumption * 4.5, 3)


# Test to check if the returned ports are correct
# 1) amount check
# 2) keys check
# 3) values check
def test_get_ports():
    shipment = Shipment(
        "78067E7F-D833-4312-A805-C1355F51F065",
        "01-01-2023",
        15649,
        5879.249,
        864.595,
        6.8,
        "MYTPP",
        "TRGEM",
        9913547,
    )
    
    assert len(shipment.get_ports()) == 2
    assert shipment.get_ports().keys() == {"origin", "destination"} 
    assert str(shipment.get_ports()) == str({
        "origin": Port(
            "MYTPP",
            55750,
            "Tanjung Pelepas",
            "Tanjung Pelepas",
            "Johor",
            "Malaysia"
        ),
        "destination": Port(
            "TRGEM",
            48947,
            "Gemlik",
            "Gemlik",
            "Bursa",
            "Turkey"
        )
    })


# Test if the returned shipments contain the required shipment(s)
def test_get_shipments_port():
    port = Port("NZWLG", 61447, "Wellington", "Wellington", "Wellington", "New Zealand")

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
