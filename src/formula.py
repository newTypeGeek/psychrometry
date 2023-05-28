import numpy as np

# Warning: Formula (i.e. functions) below is not valid if you change these two parameters
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


def vapor_pressure(humidity_ratio: np.ndarray) -> np.ndarray:
    """
    Calculate the vapor pressure from humidity ratio

    Args:
        humidity_ratio: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
        Vapor pressure, [Pa]

    """
    return humidity_ratio / (GAS_CONSTANT_RATIO + humidity_ratio) * ATMOSPHERIC_PRESSURE


def relative_humidity(dry_bulb: np.ndarray, humidity_ratio: np.ndarray) -> np.ndarray:
    """
    Calculate the relative humidity from dry bulb temperature and humidity ratio

    Args:
        dry_bulb: Dry bulb temperature, [°C]
        humidity_ratio: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
        Relative humidity, [%]

    """
    return vapor_pressure(humidity_ratio) / saturated_vapor_pressure(dry_bulb) * 100


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


def specific_enthalpy(dry_bulb: np.ndarray, humidity_ratio: np.ndarray) -> np.ndarray:
    """
    Calculate the specific enthalpy from dry bulb temperature and humidity ratio

    Args:
        dry_bulb: Dry bulb temperature, [°C]
        humidity_ratio: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
       Specific enthalpy, [kJ/kg]

    """
    return 1.006 * dry_bulb + humidity_ratio * (2501 + 1.86 * dry_bulb)


def dew_point_temperature(dry_bulb: np.ndarray, humidity_ratio: np.ndarray) -> np.ndarray:
    """
    Calculate the dew point temperature from dry bulb temperature and humidity ratio (Peppers 1988)

    Args:
        dry_bulb: Dry bulb temperature, [°C]
        humidity_ratio: Humidity ratio (vapor mass / dry air mass) [kg/kg]

    Returns:
       Dew point temperature, [°C]

    """

    p = vapor_pressure(humidity_ratio)
    alpha = np.log(p/1000)

    return 6.54 + 14.526 * alpha + 0.7389 * alpha**2 + 0.09486 * alpha**3 + 0.4569 * p**0.1984
