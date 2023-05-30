import enum


class ThermoAttribute(enum.Enum):
    DRY_BULB = "dry_bulb"
    RELATIVE_HUMIDITY = "relative_humidity"
    HUMIDITY_RATIO = "humidity_ratio"
    WET_BULB = "wet_bulb"
    DEW_POINT = "dew_point"
    SPECIFIC_ENTHALPY = "specific_enthalpy"
