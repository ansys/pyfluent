import pytest

import ansys.fluent.core.quantity as q


def test_viscosity():
    v = q.Quantity(1, "P")  # poise
    conversion_output = v.convertTo("kg m^-1 s^-1")
    assert conversion_output.value == 0.1


def test_dynamic_viscosity():
    vd = q.Quantity(1, "Pa s")
    conversion_output = vd.convertTo("P")
    assert conversion_output.value == 10.0


def test_viscosity_slugs():
    vd = q.Quantity(1, "slugs ft^-1 s^-1")
    conversion_output = vd.convertTo("kg m^-1 s^-1")
    assert conversion_output.value == pytest.approx(47.880, 0.0002)


def test_viscosity_lb():
    vd = q.Quantity(1, "lb ft^-1 s^-1")
    conversion_output = vd.convertTo("kg m^-1 s^-1")
    assert conversion_output.value == pytest.approx(1.488164, 0.000001)


def test_volume():
    v = q.Quantity(1, "gal")
    conversion_output = v.convertTo("m^3")
    assert conversion_output.value == pytest.approx(0.00378541)


def test_youngs_modulus():
    ym = q.Quantity(1, "lbf ft^-2")
    conversion_output = ym.convertTo("N m^-2")
    assert conversion_output.value == pytest.approx(47.89, 0.1)


def test_temperature():
    tempC = q.Quantity(1, "degC")  # celsius
    conversion_output_1 = tempC.convertTo("degK")
    assert conversion_output_1.value == 274.15
    conversion_output_2 = tempC.convertTo("degR")
    assert conversion_output_2.value == pytest.approx(493.46, 0.1)
    conversion_output_3 = tempC.convertTo("degF")
    assert conversion_output_3.value == pytest.approx(33.79, 0.1)


def test_collision_rate():
    cr = q.Quantity(1, "ft^-3 s^-1")
    conversion_output = cr.convertTo("m^-3 s^-1")
    assert conversion_output.value == pytest.approx(35.3147, 0.001)


def test_area_inverse():
    in_sq_m = q.Quantity(1, "m^-2")
    conversion_output = in_sq_m.convertTo("cm^-2")
    assert conversion_output.value == pytest.approx(0.0001)


def test_area():
    in_sq_m = q.Quantity(1, "m^2")
    conversion_output = in_sq_m.convertTo("in^2")
    assert conversion_output.value == pytest.approx(1550, 0.1)


def test_angular_velocity():
    degps = q.Quantity(1, "deg/s")
    conversion_output = degps.convertTo("rad/s")
    assert conversion_output.value == pytest.approx(0.01745, 0.001)


def test_hz_hertz():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_hz_rad():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_hz_radian():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_hz_rpm():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_hz_rps():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_hz_cps():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_hertz_hz():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_hertz_rad():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_hertz_radian():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_hertz_rpm():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_hertz_rps():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_hertz_cps():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_rad_hz():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_rad_hertz():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_rad_radian():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_rad_rpm():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_rad_rps():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_rad_cps():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_radian_hz():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_radian_hertz():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_radian_rad():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_radian_rpm():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_radian_rps():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_radian_cps():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_rpm_hz():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_rpm_hertz():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_rpm_radian():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_rpm_rad():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_rpm_rps():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_rpm_cps():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_rps_hz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_rps_hertz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_rps_radian():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_rps_rad():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_rps_rpm():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_rps_cps():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("cps")


def test_cps_hz():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("Hz")


def test_cps_hertz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("hertz")


def test_cps_radian():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("radian/s")


def test_cps_rad():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rad/s")


def test_cps_rpm():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rpm")


def test_cps_rps():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convertTo("rps")


def test_dyne():
    x = q.Quantity(1, "dyn cm^-2")
    conversion_output = x.convertTo("N m^-2")
    assert conversion_output.value == pytest.approx(0.1)


def test_gal():
    x = q.Quantity(1, "gal^-1")
    conversion_output = x.convertTo("m^-3")
    assert conversion_output.value == pytest.approx(264.17, 0.002)


def test_mph():
    x = q.Quantity(1, "m s^-1")
    conversion_output = x.convertTo("mph")
    assert conversion_output.value == pytest.approx(2.23694, 0.00002)


def test_inches_water():
    x = q.Quantity(1, "inch_H2O_39F")
    conversion_output = x.convertTo("Pa")
    assert conversion_output.value == pytest.approx(249, 0.1)


def test_torr():
    x = q.Quantity(1, "torr")
    conversion_output = x.convertTo("Pa")
    assert conversion_output.value == pytest.approx(133.3220, 0.0003)


def test_psi():
    x = q.Quantity(1, "psi")
    conversion_output = x.convertTo("Pa")
    assert conversion_output.value == pytest.approx(6894.757, 0.0002)


def test_atm():
    x = q.Quantity(1, "atm")
    conversion_output = x.convertTo("Pa")
    assert conversion_output.value == pytest.approx(101325.0)


def test_mole_con_henry_const():
    x = q.Quantity(1, "atm m^3 kg mol^-1")
    conversion_output = x.convertTo("Pa m^3 kg mol^-1")
    assert conversion_output.value == pytest.approx(101325.0)


def test_pdl():
    x = q.Quantity(1, "pdl")
    conversion_output = x.convertTo("N")
    assert conversion_output.value == pytest.approx(0.13826, 0.0001)


def test_ozf():
    x = q.Quantity(1, "ozf")  # force_ounce
    conversion_output = x.convertTo("N")
    assert conversion_output.value == pytest.approx(0.27802, 0.0001)


def test_lbf():
    x = q.Quantity(1, "lbf")  # force_pound
    conversion_output = x.convertTo("N")
    assert conversion_output.value == pytest.approx(4.44820, 0.00002)


def test_kgf():
    x = q.Quantity(1, "kgf")
    conversion_output = x.convertTo("N")
    assert conversion_output.value == pytest.approx(9.806805, 0.0002)


def test_cal():
    x = q.Quantity(1, "cal")
    conversion_output = x.convertTo("J")
    assert conversion_output.value == pytest.approx(4.1868, 0.002)


def test_kcal():
    x = q.Quantity(1, "kcal")
    conversion_output = x.convertTo("J")
    assert conversion_output.value == pytest.approx(4186.8, 2)


def test_hp():
    x = q.Quantity(1, "hp")
    conversion_output = x.convertTo("W")
    assert conversion_output.value == pytest.approx(745.70, 0.01)


def test_ohm():
    x = q.Quantity(1, "ohm cm")
    conversion_output = x.convertTo("ohm m")
    assert conversion_output.value == 0.01


def test_hp_h():
    x = q.Quantity(1, "hp h")  # hp_hour
    conversion_output = x.convertTo("J")
    assert conversion_output.value == pytest.approx(2.6845 * 10**6, 19)


def test_erg():
    x = q.Quantity(1, "erg")
    conversion_output = x.convertTo("J")
    assert conversion_output.value == pytest.approx(1.0 * 10**-7)


def test_energy_density():
    x = q.Quantity(1, "BTU ft^-2")
    conversion_output = x.convertTo("J m^-2")
    assert conversion_output.value == pytest.approx(11356.36, 0.2)


def test_degree_rankine():
    x = q.Quantity(1, "BTU lb^-1 degR^-1")
    conversion_output = x.convertTo("J kg^-1 degK^-1")
    assert conversion_output.value == pytest.approx(4186.69, 0.2)


def test_degree_fahrenheit():
    x = q.Quantity(1, "BTU lb^-1 degF^-1")
    conversion_output = x.convertTo("J kg^-1 degK^-1")
    assert conversion_output.value == pytest.approx(4186.69, 0.2)


def test_degree_celsius():
    x = q.Quantity(1, "cal g^-1 degC^-1")
    conversion_output = x.convertTo("J kg^-1 degK^-1")
    assert conversion_output.value == pytest.approx(4186.69, 2)


def test_mol():
    x = q.Quantity(1, "lb mol ft^-3 s^-1")
    conversion_output = x.convertTo("kg mol m^-3 s^-1")
    assert conversion_output.value == pytest.approx(16.01846, 0.000003)


def test_rpm():
    x = q.Quantity(1, "rpm")
    conversion_output = x.convertTo("rad s^-1")
    assert conversion_output.value == pytest.approx(0.1047198, 0.000001)


if __name__ == "__main__":
    v1 = q.Quantity(10.2, "m/s")  # Instantiation
    print(v1)
    print(v1.convertTo("cm/s"))  # conversion m/s to cm/s
    print(v1.convertTo("ft/s"))  # conversion m/s to ft/s
    print(v1 + 15.7)  # scalar addition
    print(v1 - 5.9)  # scalar subtraction
    print(v1 * 2)  # scalar multiplication
    print(v1 / 2)  # scalar division

    print("\n Quantity class instance arithmetic \n")
    v2 = q.Quantity(15.9, "m/s")
    print(v2 + v1)
    print(v2 - v1)
    print(v2 * v1)
    print(v2 / v1)

    print("\n mass-flux \n")
    rho1 = q.Quantity(1.225, "kg/m^3")
    mass_flux1 = 0.2 * v1 * rho1
    print(mass_flux1)

    print("\n acceleration \n")
    a1 = q.Quantity(1, "m/s^2")
    print(a1)
    print(a1.convertTo("cm/s^2"))  # conversion m/s^-2 to cm/s^-2
    print(a1.convertTo("ft/s^2"))  # conversion m/s^-2 to ft/s^-2

    print("\n angle \n")
    d1 = q.Quantity(1, "deg")
    r1 = q.Quantity(1, "rad")
    print(d1)
    print(r1)
    print(d1.convertTo("rad"))  # conversion deg to rad
    print(r1.convertTo("deg"))  # conversion rad to deg

    print("\n angluar-velocity \n")
    degps = q.Quantity(1, "deg/s")
    radps = q.Quantity(1, "rad/s")
    revpm = q.Quantity(1, "revolution/min")
    print(radps.convertTo("deg/s"))
    print(degps.convertTo("rad/s"))

    print("\n area \n")
    sq_m = q.Quantity(1, "m^2")
    print(sq_m)
    print(sq_m.convertTo("cm^2"))
    print(sq_m.convertTo("mm^2"))
    print(sq_m.convertTo("ft^2"))
    print(sq_m.convertTo("in^2"))

    print("\n area-inverse \n")
    in_sq_m = q.Quantity(1, "m^-2")
    print(in_sq_m)
    print(in_sq_m.convertTo("cm^-2"))
    print(in_sq_m.convertTo("mm^-2"))
    print(in_sq_m.convertTo("ft^-2"))
    print(in_sq_m.convertTo("in^-2"))

    print("\n collision-rate \n")
    cr = q.Quantity(1, "ft^-3 s^-1")
    print(cr)
    print(cr.convertTo("m^-3 s^-1"))

    print("\n temperature \n")
    tempC = q.Quantity(1, "degC")  # celsius
    print(tempC)
    print(tempC.convertTo("degK"))  # kelvin
    print(tempC.convertTo("degR"))  # rankine
    print(tempC.convertTo("degF"))  # fahrenheit

    print("\n youngs-modulus \n")
    ym = q.Quantity(1, "lbf ft^-2")
    print(ym)
    print(ym.convertTo("N m^-2"))

    ym2 = q.Quantity(1, "dyn cm^-2")
    print(ym2)
    print(ym2.convertTo("N m^-2"))

    print("\n volume \n")
    v = q.Quantity(1, "gal")
    print(v)
    print(v.convertTo("m^3"))

    print("\n viscosity \n")
    v = q.Quantity(1, "P")  # poise
    print(v)
    print(v.convertTo("kg m^-1 s^-1"))
