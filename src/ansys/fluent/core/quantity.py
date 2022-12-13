from collections import OrderedDict


class _UnitsTable(object):
    fundamental_units = {
        "kg": "M",
        "g": "M",
        "lb": "M",
        "lbm": "M",
        "slug": "M",
        "m": "L",
        "cm": "L",
        "ft": "L",
        "in": "L",
        "s": "T",
        "A": "I",
        "K": "Temp",
        "C": "Temp",
        "F": "Temp",
        "R": "Temp",
        "mol": "N",
        "slugmol": "N",
        "cd": "Iv",
        "sr": "SAngle",
        "radian": "Angle",
        "degree": "Angle",
    }

    derived_units = {
        "N": "kg m s^-2",
        "Pa": "N m^-2",
        "W": "N m s^-1",
        "J": "N m",
        "V": "A ohm",
        "farad": "N m V^-2",
        "H": "N m A^-2",
        "S": "ohm^-1",
        "Wb": "N m A^-1",
        "T": "Wb m^-2",
        "dyne": "g cm s^-2",
        "erg": "dyne cm",
        "pdl": "lbm ft s^-2",
        "BTU": "J",
        "psi": "lbf in^-2",
        "lbf": "slug ft s^-2",
        "psf": "lbf ft^-2",
        "ohm": "kg m^2 s^-3 A^-2",
        "Hz": "s^-1",
        "cal": "J",
        "delta_K": "K",
        "delta_C": "C",
        "delta_F": "F",
        "delta_R": "R",
        "coulomb": "A s",
    }

    derived_units_with_conversion_factor = {
        "l": (0.001, "m^3"),
        "gal": (0.0037854117839999993, "m^3"),
        "BTU": (1055.056, "J"),
        "cal": (4.184, "J"),
    }

    multipliers = {
        "d": 10**-1,
        "c": 10**-2,
        "m": 10**-3,
        "u": 10**-6,
        "n": 10**-9,
        "p": 10**-12,
        "f": 10**-15,
        "a": 10**-18,
        "z": 10**-21,
        "y": 10**-24,
        "da": 10**1,
        "h": 10**2,
        "k": 10**3,
        "M": 10**6,
        "G": 10**9,
        "T": 10**12,
        "P": 10**15,
        "E": 10**18,
        "Z": 10**21,
        "Y": 10**24,
    }

    dimension_order = OrderedDict(
        [
            ("Mass", "M"),
            ("Length", "L"),
            ("Time", "T"),
            ("Temperature", "Temp"),
            ("Angle", "Angle"),
            ("ChemicalAmount", "N"),
            ("Light", "Iv"),
            ("Current", "I"),
            ("SolidAngle", "SAngle"),
            ("", ""),
        ]
    )

    conversion_map = {
        "kg": 1,
        "g": 0.001,
        "lb": 0.45359237,
        "lbm": 0.45359237,
        "slug": 14.59390293720637,
        "m": 1,
        "cm": 0.01,
        "ft": 0.30479999999999996,
        "in": 0.0254,
        "s": 1,
        "A": 1,
        "mol": 1,
        "slugmol": 14593.9,
        "cd": 1,
        "sr": 1,
        "radian": 1,
        "degree": 0.017453292519943295,
        "K": 1,
        "C": 1,
        "F": 0.5555555555555556,
        "R": 0.5555555555555556,
        "delta_K": 1,
        "delta_C": 1,
        "delta_F": 0.5555555555555556,
        "delta_R": 0.5555555555555556,
    }

    si_map = {
        "kg": "kg",
        "g": "kg",
        "lb": "kg",
        "lbm": "kg",
        "slug": "kg",
        "m": "m",
        "cm": "m",
        "ft": "m",
        "in": "m",
        "s": "s",
        "A": "A",
        "mol": "mol",
        "slugmol": "mol",
        "cd": "cd",
        "sr": "sr",
        "radian": "radian",
        "degree": "radian",
        "K": "K",
        "C": "K",
        "F": "K",
        "R": "K",
        "": "",
    }

    temperature_conversions = {
        # from : { to : formula }
        "C": {
            "K": lambda c: c + 273.15,
            "R": lambda c: (c + 273.15) * 1.8,
            "F": lambda c: c * 9 / 5 + 32,
            "C": lambda c: c,
        },
        "F": {
            "K": lambda f: (f - 32) * 5 / 9 + 273.15,
            "R": lambda f: f + 459.67,
            "F": lambda f: f,
            "C": lambda f: (f - 32) * 5 / 9,
        },
        "R": {
            "K": lambda r: r / 1.8,
            "R": lambda r: r,
            "F": lambda r: r - 459.67,
            "C": lambda r: (r - 491.67) / 1.8,
        },
        "K": {
            "K": lambda k: k,
            "R": lambda k: k * 1.8,
            "F": lambda k: k * 1.8 - 459.67,
            "C": lambda k: k - 273.15,
        },
    }


def get_si_conversion_factor(unit_str):
    return (
        _UnitsTable.conversion_map[unit_str]
        if unit_str in _UnitsTable.conversion_map.keys()
        else 1
    )


def filter_multiplier(unit_str, predicate=None):
    result = False
    matched = ""
    for item in _UnitsTable.multipliers.keys():
        result = predicate(item, unit_str) if predicate else item == unit_str
        if result:
            matched = item
            result = True
            temp_unit_str = unit_str[len(item) :]
            if (
                temp_unit_str in _UnitsTable.fundamental_units
                or temp_unit_str in _UnitsTable.derived_units
            ):
                break
            else:
                result = False
                continue
    return result, matched


def remove_multiplier(unit_str):
    has_multiplier, prefix = filter_multiplier(
        unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
    )
    if has_multiplier:
        unit_str = unit_str[len(prefix) :]
    return unit_str


def is_temperature_quantity(dim_obj):
    temp_dim = dim_obj["Temp"]
    total_dims_sum = sum([abs(val) for val in dim_obj.values()])
    return temp_dim == 1 and total_dims_sum == temp_dim


class Unit(object):
    def __init__(self, unit_str):
        self._unit = unit_str
        self._si_multiplier = 1
        self._si_offset = 0
        self._si_unit = ""
        self._offset_power = 1
        self._compute_multipliers(unit_str, 1)
        self._compute_offset(unit_str)
        self._reduce_to_si_unit(self._si_unit)

    @property
    def user_unit(self):
        return self._unit

    @property
    def si_factor(self):
        return self._si_multiplier

    @property
    def si_unit(self):
        return self._si_unit

    @property
    def si_offset(self):
        return self._si_offset

    @property
    def offset_power(self):
        return self._offset_power

    def __call__(self):
        return self.user_unit

    def _reduce_to_si_unit(self, unit_str):
        term_power_dict = OrderedDict()
        unit_split = unit_str.split(" ")

        for term in unit_split:
            if "^" in term:
                term_split = term.split("^")
                if term_split[0] in term_power_dict.keys():
                    term_power_dict[term_split[0]] += float(term_split[1])
                else:
                    term_power_dict[term_split[0]] = float(term_split[1])
            else:
                if term in term_power_dict.keys():
                    term_power_dict[term] += 1.0
                else:
                    term_power_dict[term] = 1.0

        self._si_unit = ""

        for key, power in term_power_dict.items():
            spacechar = " " if len(self._si_unit) > 0 else ""

            if power == 1.0:
                self._si_unit += spacechar + key
            elif power != 0.0:
                self._si_unit += (
                    spacechar
                    + key
                    + "^"
                    + str(int(power) if power.is_integer() else power)
                )
            else:
                self._si_unit += spacechar + key

    def _compute_multipliers(self, unit_str, power):
        if len(unit_str) == 0:
            return

        unit_list = unit_str.split(" ")

        for term in unit_list:
            unit_str = term
            term_power = 1

            if "^" in unit_str:
                unit_str, term_power = unit_str[: unit_str.index("^")], float(
                    unit_str[unit_str.index("^") + 1 :]
                )

            term_power *= power
            has_multiplier = not (
                unit_str in _UnitsTable.fundamental_units
                or unit_str in _UnitsTable.derived_units
            )

            if has_multiplier:
                _, prefix = filter_multiplier(
                    unit_str,
                    lambda item, unit: len(unit) > 0.0 and unit.startswith(item),
                )

                if len(prefix):
                    self._si_multiplier *= _UnitsTable.multipliers[prefix] ** term_power

                unit_str = remove_multiplier(unit_str)

            if unit_str in _UnitsTable.fundamental_units:
                spacechar = " " if len(self._si_unit) > 0 else ""

                if term_power == 1.0:
                    self._si_unit += spacechar + _UnitsTable.si_map[unit_str]
                elif term_power != 0.0:
                    self._si_unit += (
                        spacechar + _UnitsTable.si_map[unit_str] + "^" + str(term_power)
                    )
                elif term_power == 0.0:
                    self._si_unit += ""
                else:
                    self._si_unit += spacechar + _UnitsTable.si_map[unit_str]

                self._si_multiplier *= get_si_conversion_factor(unit_str) ** term_power

            elif unit_str in _UnitsTable.derived_units_with_conversion_factor:
                (
                    conversion_factor,
                    unit_str,
                ) = _UnitsTable.derived_units_with_conversion_factor[unit_str]
                self._si_multiplier *= conversion_factor**term_power
                self._compute_multipliers(unit_str, term_power)
            elif unit_str in _UnitsTable.derived_units:
                self._compute_multipliers(
                    _UnitsTable.derived_units[unit_str], term_power
                )

    @staticmethod
    def _power_sum(base, unit_str):
        if unit_str in ["K", "C", "F", "R"]:
            if "^" in unit_str:
                return sum(
                    [
                        float(term.split("^")[1])
                        for term in unit_str.split(" ")
                        if term.split("^")[0] == base
                    ]
                )
            else:
                return 1.0

    def _compute_offset(self, unit_str):
        if unit_str == "C":
            self._si_offset = 273.15
            self._offset_power = self._power_sum("C", unit_str)
        elif unit_str == "F":
            self._si_offset = 255.3722
            self._offset_power = self._power_sum("F", unit_str)
        else:
            self._si_offset = 0
            self._offset_power = 1.0

    def _quantity_type(self):
        temperature_units = ["K", "C", "F", "R"]
        qty_type = None
        for temp_unit in temperature_units:
            unit_power = Unit._power_sum(temp_unit, self._unit)
            if temp_unit in self._unit and unit_power == 1.0:
                qty_type = "Temperature"
            elif "delta_" in self._unit:
                qty_type = "Temperature Difference"
            elif temp_unit in self._unit and unit_power not in [0.0, 1.0]:
                qty_type = "Temperature Difference"
        return qty_type


class Dimension(object):
    def __init__(self, unit_str):
        self._dimensions = {
            "M": 0.0,
            "L": 0.0,
            "T": 0.0,
            "Temp": 0.0,
            "I": 0.0,
            "N": 0.0,
            "Iv": 0.0,
            "Angle": 0.0,
            "SAngle": 0.0,
            "": 0.0,
        }
        self._parser(unit_str)

    def _add_or_update_dimension(self, dim_dict):
        for key in dim_dict.keys():
            self._dimensions[key] += dim_dict[key]

    def _parser(self, unit, power=1):
        if len(unit) == 0:
            return

        unit_list = unit.split(" ")
        for term in unit_list:
            unit_dim = ""
            has_multiplier = not (
                term in _UnitsTable.fundamental_units
                or term in _UnitsTable.derived_units
            )
            unit_str = remove_multiplier(term) if has_multiplier else term
            term_power = 1

            if "^" in term:
                unit_str, term_power = term[: term.index("^")], float(
                    term[term.index("^") + 1 :]
                )
                has_multiplier = not (
                    unit_str in _UnitsTable.fundamental_units
                    or unit_str in _UnitsTable.derived_units
                )
                unit_str = remove_multiplier(unit_str) if has_multiplier else unit_str

            term_power *= power
            unit_dim = self._get_dim(unit_str, term_power)

            if unit_dim != None:
                self._add_or_update_dimension(unit_dim)

    def as_dict(self):
        return self._dimensions

    def _get_dim(self, unit_str, power):
        if unit_str in _UnitsTable.fundamental_units:
            return {_UnitsTable.fundamental_units[unit_str]: power}
        elif unit_str in _UnitsTable.derived_units:
            self._parser(_UnitsTable.derived_units[unit_str], power)
        elif unit_str in _UnitsTable.derived_units_with_conversion_factor:
            _, unit_str = _UnitsTable.derived_units_with_conversion_factor[unit_str]
            self._parser(unit_str, power)
        else:
            raise ValueError("Not implemented")


def get_si_unit_from_dim(dim_list):
    si_unit = ""
    dim_to_unit_map = UnitSystem("SI").base_units()

    for key, power in zip(_UnitsTable.dimension_order.values(), dim_list):
        unit_str = dim_to_unit_map[key]
        spacechar = " " if len(si_unit) > 0 else ""
        if power == 1.0:
            si_unit += spacechar + unit_str
        elif power != 0.0:
            si_unit += (
                spacechar
                + unit_str
                + "^"
                + str(int(power) if power.is_integer() else power)
            )
    return si_unit


class UnitSystem:

    _dim_to_unit_sys_map = {
        "SI": {
            "M": "kg",
            "L": "m",
            "T": "s",
            "Temp": "K",
            "I": "A",
            "N": "mol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
        "CGS": {
            "M": "g",
            "L": "cm",
            "T": "s",
            "Temp": "K",
            "I": "A",
            "N": "mol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
        "BT": {
            "M": "slug",
            "L": "ft",
            "T": "s",
            "Temp": "R",
            "I": "A",
            "N": "slugmol",
            "Iv": "cd",
            "Angle": "radian",
            "SAngle": "sr",
            "": "",
        },
    }

    _supported_unit_sys = ("SI", "CGS", "BT")

    def __init__(self, unit_sys):
        self._unit_system = unit_sys.upper()

        if self._unit_system not in UnitSystem._supported_unit_sys:
            raise ValueError(
                "Unsupported unit system, only 'SI', 'CGS', 'BT' is allowed."
            )

    def _get_unit_from_dim(self, dim_list):
        unit = ""

        base_units = UnitSystem._dim_to_unit_sys_map[self._unit_system]
        for key, power in zip(_UnitsTable.dimension_order.values(), dim_list):
            spacechar = " " if len(unit) > 0 else ""
            if power == 1:
                unit += spacechar + base_units[key]
            elif power != 0:
                unit += (
                    spacechar
                    + base_units[key]
                    + "^"
                    + str(int(power) if power.is_integer() else power)
                )
        return unit

    def convert(self, quantity):
        if not isinstance(quantity, Quantity):
            raise TypeError("Not instance of Quantity.")
        dims = quantity.get_dimensions_list()
        unit_str = self._get_unit_from_dim(dims)
        return quantity.to(unit_str)

    def base_units(self):
        return UnitSystem._dim_to_unit_sys_map[self._unit_system]


class QuantityError(ValueError):
    def __init__(self, from_unit, to_unit):
        self.from_unit = from_unit
        self.to_unit = to_unit

    def __str__(self):
        return f"{self.unit} and {self.to_unit} have incompatible dimensions."


unit_quantity_map = {
    "Mass": "kg",
    "Length": "m",
    "Time": "s",
    "Temperature": "K",
    "Current": "A",
    "SubstanceAmount": "mol",
    "Light": "cd",
    "Angle": "radian",
    "SolidAngle": "sr",
    "Acceleration": "m s^-2",
    "Angular Acceleration": "radian s^-2",
    "Angular Velocity": "radian s^-1",
    "Area": "m^2",
    "Capacitance": "farad",
    "Compressibility": "Pa^-1",
    "Concentration": "m^-3",
    "Contact Resistance": "m^2 s kg^-1",
    "Current Transfer Coefficient": "A m^-2 V^-1",
    "Decay Constant": "s^-1",
    "Density": "kg m^-3",
    "Density Derivative": "m^-2 s^2",
    "Density Derivative wrt Pressure": "m^-2 s^2",
    "Density Derivative wrt Temperature": "kg m^-3 K^-1",
    "Dielectric Contact Resistance": "farad^-1 m^2",
    "Dynamic Viscosity": "Pa s",
    "Electric Charge": "A s",
    "Electric Charge Density": "A s m^-3",
    "Electric Charge Transfer Coefficient": "farad m^-2",
    "Electric Conductance Per Unit Area": "S m^-2",
    "Electric Current Density": "A m^-2",
    "Electric Current Source": "A m^-3",
    "Electric Field": "V m^-1",
    "Electric Flux Density": "coulomb m^-2",
    "Electrical Conductance": "S",
    "Electrical Conductivity": "S m^-1",
    "Electrical Contact Resistance": "S^-1 m^2",
    "Electrical Permittivity": "A s V^-1 m^-1",
    "Electrical Resistance": "ohm",
    "Electrical Resistivity": "ohm m",
    "Energy Density by Mass": "J kg^-1",
    "Energy Source": "W m^-3",
    "Energy Source Coefficient": "W m^-3 K^-1",
    "Enthalpy Variance": "m^4 s^-4",
    "Epsilon": "m^2 s^-3",
    "Epsilon Flux": "W m^-2 s^-1",
    "Epsilon Flux Coefficient": "kg m^-2 s^-2",
    "Epsilon Source": "W m^-3 s^-1",
    "Epsilon Source Coefficient": "kg m^-3 s^-2",
    "Flame Surface Density Source": "m^-1 s^-1",
    "Force": "N",
    "Force Density": "N m^-3",
    "Force Intensity": "N m^-1",
    "Force Per Angular Unit": "N radian^-1",
    "Fracture Energy": "J m^-2",
    "Fracture Energy Rate": "J m^-2 s^-1",
    "Frequency": "Hz",
    "Gasket Stiffness": "Pa m^-1",
    "Heat Flux": "W m^-2",
    "Heat Flux in": "W m^-2",
    "Heat Generation": "W m^-3",
    "Heat Rate": "W",
    "Heat Transfer Coefficient": "W m^-2 K^-1",
    "Impulse": "N s",
    "Impulse Per Angular Unit": "N s radian^-1",
    "Inductance": "H",
    "Interphase Transfer Coefficient": "kg m^-2 s^-1",
    "InvTemp1": "K^-1",
    "InvTemp2": "K^-2",
    "InvTemp3": "K^-3",
    "InvTemp4": "K^-4",
    "Inverse Angle": "radian^-1",
    "Inverse Area": "m^-2",
    "Inverse Length": "m^-1",
    "Inverse Stress": "Pa^-1",
    "Kinematic Diffusivity": "m^2 s^-1",
    "MAPDL Enthalpy": "J m^-3",
    "Magnetic Field": "A m^-1",
    "Magnetic Field Intensity": "A m^-1",
    "Magnetic Flux": "Wb",
    "Magnetic Flux Density": "T",
    "Magnetic Induction": "T",
    "Magnetic Permeability": "H m^-1",
    "Magnetic Potential": "T m",
    "Mass Concentration": "kg m^-3",
    "Mass Concentration Rate": "kg m^-3 s^-1",
    "Mass Flow": "kg s^-1",
    "Mass Flow Rate Per Area": "kg s^-1 m^-2",
    "Mass Flow Rate Per Length": "kg s^-1 m^-1",
    "Mass Flow Rate Per Volume": "kg s^-1 m^-3",
    "Mass Flow in": "kg s^-1",
    "Mass Flux": "kg s^-1 m^-2",
    "Mass Flux Coefficient": "kg s^-1 m^-2",
    "Mass Flux Pressure Coefficient": "kg s^-1 m^-2 Pa^-1",
    "Mass Fraction": "kg kg^-1",
    "Mass Per Area": "kg m^-2",
    "Mass Source": "kg s^-1 m^-3",
    "Mass Source Coefficient": "kg s^-1 m^-3 Pa^-1",
    "Material Impedance": "kg m^-2 s^-1",
    "Molar Concentration": "mol m^-3",
    "Molar Concentration Henry Coefficient": "Pa m^3 mol^-1",
    "Molar Concentration Rate": "mol m^-3 s^-1",
    "Molar Energy": "J mol^-1",
    "Molar Entropy": "J mol^-1 K^-1",
    "Molar Fraction": "mol mol^-1",
    "Molar Mass": "kg kmol^-1",
    "Molar Volume": "m^3 mol^-1",
    "Moment": "N m",
    "Moment of Inertia of Area": "m^2 m^2",
    "Moment of Inertia of Mass": "kg m^2",
    "Momentum Source": "kg m^-2 s^-2",
    "Momentum Source Lin Coeff": "kg m^-3 s^-1",
    "Momentum Source Quad Coeff": "kg m^-4",
    "Normalized Value": "m m^-1",
    "Number Source": "m^-3 s^-1",
    "Omega Source": "kg m^-3 s^-2",
    "PSD Acceleration": "m^2 s^-4 Hz^-1",
    "PSD Displacement": "m^2 Hz^-1",
    "PSD Force": "N^2 Hz^-1",
    "PSD Moment": "N^2 m^2 Hz^-1",
    "PSD Pressure": "Pa^2 Hz^-1",
    "PSD Strain": "m^2 m^-2 Hz^-1",
    "PSD Stress": "Pa^2 Hz^-1",
    "PSD Velocity": "m^2 s^-2 Hz^-1",
    "Per Mass": "kg^-1",
    "Per Mass Flow": "s kg^-1",
    "Per Time": "s^-1",
    "Per Time Cubed": "s^-3",
    "Per Time Squared": "s^-2",
    "Power Spectral Density": "W Hz^-1",
    "Pressure": "Pa",
    "Pressure Derivative wrt Temperature": "Pa K^-1",
    "Pressure Derivative wrt Volume": "Pa kg m^-3",
    "Pressure Gradient": "Pa m^-1",
    "Relative Permeability": "H H^-1",
    "Relative Permittivity": "farad farad^-1",
    "Rotational Damping": "N m s radian^-1",
    "Rotational Stiffness": "N m radian^-1",
    "Section Modulus": "m^3",
    "Seebeck Coefficient": "V K^-1",
    "Shear Strain": "radian",
    "Shear Strain Rate": "s^-1",
    "Shock Velocity": "s m^-1",
    "Soot Cross Coefficient": "m^3 mol^-1 s^-1",
    "Soot PX Facto": "mol kg^-1 s^-1",
    "Specific": "kg kg^-1",
    "Specific Concentration": "mol kg^-1",
    "Specific Energy": "J kg^-1",
    "Specific Enthalpy": "J kg^-1",
    "Specific Entropy": "J kg^-1 K^-1",
    "Specific Flame Surface Density": "m^2 kg^-1",
    "Specific Heat Capacity": "J kg^-1 K^-1",
    "Specific Volume": "kg^-1 m^3",
    "Specific Weight": "N m^-3",
    "Stiffness": "N m^-1",
    "Strain": "m m^-1",
    "Strength": "Pa",
    "Stress": "Pa",
    "Stress Intensity Factor": "Pa m^0.5",
    "Stress Per Temperature": "Pa K^-1",
    "Surface Charge Density": "A s m^-2",
    "Surface Force Density": "N m^-2",
    "Surface Power Density": "W m^-2",
    "Surface Tension": "N m^-1",
    "Temperature Difference": "delta_K",
    "Temperature Gradient": "K m^-1",
    "Temperature Variance": "K^2",
    "Temperature Variance Source": "kg m^-3 s^-1 K^2",
    "Thermal Capacitance": "J K^-1",
    "Thermal Conductance": "W K^-1",
    "Thermal Conductivity": "W m^-1 K^-1",
    "Thermal Contact Resistance": "W^-1 m^2 K",
    "Thermal Expansivity": "K^-1",
    "Torque": "N m",
    "Torsional Spring Constant": "N m radian^-1",
    "Total Mass Source Pressure Coefficient": "kg s^-1 Pa^-1",
    "Total Radiative Intensity": "W m^-2 sr^-1",
    "Translational Damping": "N s m^-1",
    "Turbulent Heat Flux": "m^3 s^-3",
    "Velocity": "m s^-1",
    "Volume": "m^3",
    "Volumetric": "kg m^-3",
    "Volumetric Flow": "m^3 s^-1",
    "Volumetric Flow in": "m^3 s^-1",
    "Warping Factor": "m^6",
}


def get_unit_from_map(quantity_map_from_settings_api):
    terms = []
    term_power_list = []
    final_unit = ""
    for unit in quantity_map_from_settings_api.keys():
        unit_str = unit_quantity_map[unit]
        unit_term_list = unit_str.split(" ") if " " in unit_str else unit_str
        term_power_list.append(unit_term_list)
    power_list = list(
        map(lambda x: float(x), list(quantity_map_from_settings_api.values()))
    )
    for item in range(len(power_list)):
        if isinstance(term_power_list[item], str) and power_list[item] == 1.0:
            terms.append(term_power_list[item])
        elif isinstance(term_power_list[item], list) and power_list[item] == 1.0:
            for term in term_power_list[item]:
                terms.append(term)
        elif isinstance(term_power_list[item], str) and power_list[item] != 0.0:
            terms.append(
                term_power_list[item]
                + "^"
                + str(
                    int(power_list[item])
                    if power_list[item].is_integer()
                    else power_list[item]
                )
            )
        elif isinstance(term_power_list[item], list) and power_list[item] != 0.0:
            for term in term_power_list[item]:
                if "^" in term:
                    term_split = term.split("^")
                    resulting_power = float(term_split[1]) * power_list[item]
                    terms.append(
                        term_split[0]
                        + "^"
                        + str(
                            int(resulting_power)
                            if resulting_power.is_integer()
                            else resulting_power
                        )
                    )
                else:
                    terms.append(
                        term
                        + "^"
                        + str(
                            int(power_list[item])
                            if power_list[item].is_integer()
                            else power_list[item]
                        )
                    )
    for term in terms:
        final_unit += (" " if len(final_unit) > 0 else "") + term

    unit_term_list = final_unit.split(" ")
    unit_power_list = [
        terms.split("^") if "^" in terms else terms for terms in unit_term_list
    ]

    term_power_map = {}
    for term in unit_power_list:
        if isinstance(term, str):
            if term in term_power_map.keys():
                term_power_map[term] += 1.0
            else:
                term_power_map[term] = 1.0
        if isinstance(term, list):
            if term[0] in term_power_map.keys():
                term_power_map[term[0]] += float(term[1])
            else:
                term_power_map[term[0]] = float(term[1])

    unit_terms = []
    for term, power in term_power_map.items():
        if power == 1.0:
            unit_terms.append(term)
        elif power != 0.0:
            unit_terms.append(
                term + "^" + str(int(power) if power.is_integer() else power)
            )

    unit = ""
    for term in unit_terms:
        unit += (" " if len(unit) > 0 else "") + term
    return unit


class Quantity(float):
    """This class instantiates physical quantities using their real values and
    units.

    Attributes
    ----------
    value: Real value
        Value of quantity is stored as float.

    unit: Unit string
        Unit of quantity is stored as string.

    Methods
    -------
    get_dimensions_list()
        Extracts dimensions from unit.

    is_dimensionless()
        Determines type of quantity.

    to(to_unit)
        Converts to given unit string.

    Returns
    -------
    Quantity instance.

    All the instances of this class are converted to base SI units system to have
    consistency in all arithmetic operations.
    """

    def __init__(self, real_value, unit_str=None, quantity_map=None):
        self._value = float(real_value)
        if unit_str and quantity_map:
            raise ValueError("Either unit or quantity_map is allowed.")
        if quantity_map:
            unit_str = get_unit_from_map(quantity_map)
        self._unit = Unit(unit_str)
        self._dimension = Dimension(unit_str)
        self._si_value = (
            self._unit.si_factor * self._value + self._unit.si_offset
        ) ** self._unit.offset_power
        self._si_unit = self._unit.si_unit
        self._type = self._unit._quantity_type()

    def __new__(cls, real_value, unit_str=None, quantity_map=None):
        if unit_str and quantity_map:
            raise ValueError("Either unit or quantity_map is allowed.")
        if quantity_map:
            unit_str = get_unit_from_map(quantity_map)
        _unit = Unit(unit_str)
        return float.__new__(
            cls, (_unit.si_factor * real_value + _unit.si_offset) ** _unit.offset_power
        )

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit.user_unit

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def dimension(self):
        return self._dimension

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_str):
        self._type = type_str

    def is_dimensionless(self):
        return all([value == 0 for value in self.get_dimensions_list()])

    def get_dimensions_list(self):
        dims = self._dimension.as_dict()
        return [
            dims[_UnitsTable.dimension_order[key]]
            for key in _UnitsTable.dimension_order.keys()
        ]

    def to(self, to_unit_str):
        if not isinstance(to_unit_str, str):
            raise TypeError("Unit should be of 'str' type.")

        temp_quantity = Quantity(1, to_unit_str)

        curr_unit_dim_obj = self.dimension
        to_unit_dim_obj = temp_quantity.dimension

        if curr_unit_dim_obj.as_dict() != to_unit_dim_obj.as_dict():
            raise QuantityError(self.unit, to_unit_str)
        else:
            pass

        if is_temperature_quantity(curr_unit_dim_obj.as_dict()):
            return self._get_converted_temperature(to_unit_str)
        else:
            curr_unit_obj = self._unit
            to_unit_obj = temp_quantity._unit
            temp_quantity.value = (
                curr_unit_obj.si_factor / to_unit_obj.si_factor
            ) * self.value
            return temp_quantity

    def _get_converted_temperature(self, to_unit_str):
        from_unit_str = self.unit

        if "^" in from_unit_str:
            from_unit_str = from_unit_str.split("^")[0]

        if "^" in to_unit_str:
            to_unit_str = to_unit_str.split("^")[0]

        _, prefix = filter_multiplier(
            from_unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
        )
        from_unit_multiplier = (
            _UnitsTable.multipliers[prefix] if len(prefix) != 0 else 1.0
        )

        _, prefix = filter_multiplier(
            to_unit_str, lambda item, unit: len(unit) > 0.0 and unit.startswith(item)
        )
        to_unit_multiplier = (
            _UnitsTable.multipliers[prefix] if len(prefix) != 0 else 1.0
        )

        from_key = remove_multiplier(from_unit_str)
        to_key = remove_multiplier(to_unit_str)

        return Quantity(
            _UnitsTable.temperature_conversions[from_key][to_key](
                from_unit_multiplier * self.value
            )
            / to_unit_multiplier,
            to_unit_str,
        )

    def _get_si_unit(self, other, func):
        curr_dim = self.get_dimensions_list()
        other_dim = other.get_dimensions_list()
        temp_dim = [func(curr_dim[i], other_dim[i]) for i in range(len(other_dim))]
        temp_unit = get_si_unit_from_dim(temp_dim)
        return temp_unit

    def __pow__(self, exponent):
        new_dims = list(map(lambda x: x * exponent, self.get_dimensions_list()))
        new_si_unit = get_si_unit_from_dim(new_dims)
        new_si_value = pow(self._si_value, exponent)
        return Quantity(new_si_value, new_si_unit)

    def __str__(self):
        return f'({self.value}, "{self.unit}")'

    def __repr__(self):
        return f'Quantity ({self.value}, "{self.unit}")'

    def __mul__(self, other):
        if isinstance(other, Quantity):
            temp_value = self._si_value * other._si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x + y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            if self.type == "Temperature Difference":
                result = Quantity(float(self) * float(other), "delta_K")
                result.type = "Temperature Difference"
                return result
            return Quantity(self._si_value * other, self._si_unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            temp_value = self._si_value / other._si_value
            temp_unit = self._get_si_unit(other, lambda x, y: x - y)
            return Quantity(temp_value, temp_unit)
        elif isinstance(other, int) or isinstance(other, float):
            temp = Quantity(self._si_value / other, self._si_unit)
            return temp

    def __rtruediv__(self, other):
        if not isinstance(other, Quantity) and isinstance(other, float):
            return Quantity(other / self._si_value, self._si_unit)
        else:
            return other / self

    def validate_matching_dimensions(self, other):
        if isinstance(other, Quantity) and (
            self.get_dimensions_list() != other.get_dimensions_list()
        ):
            raise ValueError("Incompatible dimensions.")
        elif (
            (not self.is_dimensionless())
            and (not isinstance(other, Quantity))
            and isinstance(other, (float, int))
        ):
            raise TypeError("Incompatible quantities.")

    def __add__(self, other):
        self.validate_matching_dimensions(other)
        temp_types = ["Temperature", "Temperature Difference"]
        if self.type in temp_types and other.type in temp_types:
            result = Quantity(float(self) + float(other), "K")
            result.type = "Temperature"
            return result
        temp_value = float(self) + float(other)
        return Quantity(temp_value, self._si_unit)

    def __radd__(self, other):
        return Quantity(other, "") + self

    def __sub__(self, other):
        self.validate_matching_dimensions(other)
        temp_types = ["Temperature", "Temperature Difference"]
        if self.type in temp_types and other.type in temp_types:
            result = Quantity(float(self) - float(other), "delta_K")
            result.type = "Temperature Difference"
            return result
        temp_value = float(self) - float(other)
        return Quantity(temp_value, self._si_unit)

    def __rsub__(self, other):
        return Quantity(other, "") - self

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __gt__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) > float(other)

    def __ge__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) >= float(other)

    def __lt__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) < float(other)

    def __le__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) <= float(other)

    def __eq__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) == float(other)

    def __neq__(self, other):
        self.validate_matching_dimensions(other)
        return float(self) != float(other)
