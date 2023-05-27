import numpy as np

ATMOSPHERIC_PRESSURE = 101325  # Pa
GAS_CONSTANT_RATIO = 0.621945  # R_d / R_v


def saturated_vapor_pressure(dry_bulb: np.ndarray) -> np.ndarray:
    """
    Calculate the saturated vapor pressure using Hyland and Wexler 1983 which is also recommended by ASHRAE
    WARNING: This is only valid for temperatures between -100 °C and 200 °C at atmospheric pressure

    Args:
        dry_bulb: Dry bulb temperature, [°C]

    Returns:
        Saturated vapor pressure, [Pa]

    """
    t_kelvin = dry_bulb + 273.15

    log_p_sat = (
        -5.8002206e3 / t_kelvin
        + 1.3914993
        - 4.8640239e-2 * t_kelvin
        + 4.1764768e-5 * t_kelvin**2
        - 1.4452093e-8 * t_kelvin**3
        + 6.5459673 * np.log(t_kelvin)
    )

    return np.exp(log_p_sat)


def vapor_pressure(w: np.ndarray) -> np.ndarray:
    """
    Calculate the vapor pressure from humidity ratio

    Args:
        w: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
        Vapor pressure, [Pa]

    """
    return w / (GAS_CONSTANT_RATIO + w) * ATMOSPHERIC_PRESSURE


def relative_humidity(dry_bulb: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    Calculate the relative humidity from dry bulb temperature and humidity ratio

    Args:
        dry_bulb: Dry bulb temperature, [°C]
        w: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
        Relative humidity, [%]

    """
    return vapor_pressure(w) / saturated_vapor_pressure(dry_bulb) * 100


def humidity_ratio(dry_bulb: np.ndarray, relative_humidity: np.ndarray) -> np.ndarray:
    """
    Calculate the humidity ratio from dry bulb temperature and relative humidity

    Args:
        dry_bulb: Dry bulb temperature, [°C]
        relative_humidity: Relative humidity, [%]

    Returns:
        Humidity ratio (vapor mass / dry air mass) [kg/kg]

    """
    vapor_pressure = relative_humidity / 100 * saturated_vapor_pressure(dry_bulb)
    return GAS_CONSTANT_RATIO * vapor_pressure / (ATMOSPHERIC_PRESSURE - vapor_pressure)