import numpy as np

import formula
import schema


class IsoLine:
    def __init__(self) -> None:
        self._dry_bulbs = np.arange(-10, 50 + 0.1, 0.1)
        self._num_data_points = len(self._dry_bulbs)

    def get_iso_line_thermo_attrs(
        self, by: schema.ThermoAttribute, start: float, end: float, step: float
    ) -> dict[float, dict[schema.ThermoAttribute, np.ndarray]]:
        iso_to_thermo_properties = {}

        for iso_value in np.arange(start, end + step, step):
            iso_to_thermo_properties[iso_value] = {}
            thermo_to_attr = self._compute_thermo_attrs(by, iso_value)
            iso_to_thermo_properties[iso_value] = thermo_to_attr

        return iso_to_thermo_properties

    def _compute_thermo_attrs(self, by: str, iso_value: float) -> dict[schema.ThermoAttribute, np.ndarray]:
        if by == schema.ThermoAttribute.RELATIVE_HUMIDITY:
            humidity_ratios = formula.humidity_ratio(self._dry_bulbs, iso_value)
            relative_humidities = np.array([iso_value] * self._num_data_points)
            wet_bulbs = formula.wet_bulb_temperature(self._dry_bulbs, iso_value)
        elif by == schema.ThermoAttribute.WET_BULB:
            humidity_ratios = formula.humidity_ratio_by_dry_bulb_and_wet_bulb(self._dry_bulbs, iso_value)
            relative_humidities = formula.relative_humidity(self._dry_bulbs, humidity_ratios)
            wet_bulbs = np.array([iso_value] * self._num_data_points)
        else:
            raise NotImplementedError(f"Unsupported {by=}")

        dew_points = formula.dew_point_temperature(humidity_ratios)
        spec_enthalpies = formula.specific_enthalpy(self._dry_bulbs, humidity_ratios)

        thermo_to_attr = {
            schema.ThermoAttribute.DRY_BULB: self._dry_bulbs,
            schema.ThermoAttribute.HUMIDITY_RATIO: humidity_ratios,
            schema.ThermoAttribute.RELATIVE_HUMIDITY: relative_humidities,
            schema.ThermoAttribute.WET_BULB: wet_bulbs,
            schema.ThermoAttribute.DEW_POINT: dew_points,
            schema.ThermoAttribute.SPECIFIC_ENTHALPY: spec_enthalpies,
        }

        return self._filter_physical_data(by, thermo_to_attr)

    def _filter_physical_data(
        self, iso_by: schema.ThermoAttribute, thermo_to_attr: dict[schema.ThermoAttribute, np.ndarray]
    ):
        if iso_by == schema.ThermoAttribute.RELATIVE_HUMIDITY:
            return thermo_to_attr
        else:
            is_physical = (0 <= thermo_to_attr[schema.ThermoAttribute.RELATIVE_HUMIDITY]) & (
                thermo_to_attr[schema.ThermoAttribute.RELATIVE_HUMIDITY] <= 100
            )

            for thermo_attr in schema.ThermoAttribute:
                thermo_to_attr[thermo_attr] = thermo_to_attr[thermo_attr][is_physical]

            return thermo_to_attr
