import pytest

import ansys.fluent.core.quantity as q


def test_viscosity():
    v = q.Quantity(1, "P")  # poise
    conversion_output = v.convert("kg m^-1 s^-1")
    assert conversion_output.value == 0.1


def test_dynamic_viscosity():
    vd = q.Quantity(1, "Pa s")  # poise
    conversion_output = vd.convert("P")
    assert conversion_output.value == 10.0


def test_volume():
    v = q.Quantity(1, "gal")
    conversion_output = v.convert("m^3")
    assert conversion_output.value == pytest.approx(0.00378541)


def test_youngs_modulus():
    ym = q.Quantity(1, "lbf ft^-2")
    conversion_output = ym.convert("N m^-2")
    assert conversion_output.value == pytest.approx(47.89, 0.1)


def test_temperature():
    tempC = q.Quantity(1, "degC")  # celsius
    conversion_output_1 = tempC.convert("degK")
    assert conversion_output_1.value == 274.15
    conversion_output_2 = tempC.convert("degR")
    assert conversion_output_2.value == pytest.approx(493.46, 0.1)
    conversion_output_3 = tempC.convert("degF")
    assert conversion_output_3.value == pytest.approx(33.79, 0.1)


def test_collision_rate():
    cr = q.Quantity(1, "ft^-3 s^-1")
    conversion_output = cr.convert("m^-3 s^-1")
    assert conversion_output.value == pytest.approx(35.3147, 0.001)


def test_area_inverse():
    in_sq_m = q.Quantity(1, "m^-2")
    conversion_output = in_sq_m.convert("cm^-2")
    assert conversion_output.value == pytest.approx(0.0001)


def test_area():
    in_sq_m = q.Quantity(1, "m^2")
    conversion_output = in_sq_m.convert("in^2")
    assert conversion_output.value == pytest.approx(1550, 0.1)


def test_angular_velocity():
    degps = q.Quantity(1, "deg/s")
    conversion_output = degps.convert("rad/s")
    assert conversion_output.value == pytest.approx(0.01745, 0.001)


def test_hz_hertz():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_hz_rad():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_hz_radian():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_hz_rpm():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_hz_rps():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_hz_cps():
    f = q.Quantity(1, "Hz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_hertz_hz():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_hertz_rad():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_hertz_radian():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_hertz_rpm():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_hertz_rps():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_hertz_cps():
    f = q.Quantity(1, "hertz")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_rad_hz():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_rad_hertz():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_rad_radian():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_rad_rpm():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_rad_rps():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_rad_cps():
    f = q.Quantity(1, "rad/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_radian_hz():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_radian_hertz():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_radian_rad():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_radian_rpm():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_radian_rps():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_radian_cps():
    f = q.Quantity(1, "radian/s")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_rpm_hz():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_rpm_hertz():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_rpm_radian():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_rpm_rad():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_rpm_rps():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_rpm_cps():
    f = q.Quantity(1, "rpm")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_rps_hz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_rps_hertz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_rps_radian():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_rps_rad():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_rps_rpm():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_rps_cps():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("cps")


def test_cps_hz():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("Hz")


def test_cps_hertz():
    f = q.Quantity(1, "rps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("hertz")


def test_cps_radian():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("radian/s")


def test_cps_rad():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rad/s")


def test_cps_rpm():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rpm")


def test_cps_rps():
    f = q.Quantity(1, "cps")
    with pytest.raises(Exception) as e_info:
        conversion_output = f.convert("rps")


def test_dyne():
    x = q.Quantity(1, "dyn cm^-2")
    conversion_output = x.convert("N m^-2")
    assert conversion_output.value == pytest.approx(0.1)


def test_gal():
    x = q.Quantity(1, "gal^-1")
    conversion_output = x.convert("m^-3")
    assert conversion_output.value == pytest.approx(264.17, 0.002)


def test_mph():
    x = q.Quantity(1, "m s^-1")
    conversion_output = x.convert("mph")
    assert conversion_output.value == pytest.approx(2.23694, 0.00002)


def test_inches_water():
    x = q.Quantity(1, "inch_H2O_39F")
    conversion_output = x.convert("Pa")
    assert conversion_output.value == pytest.approx(249, 0.1)


def test_torr():
    x = q.Quantity(1, "torr")
    conversion_output = x.convert("Pa")
    assert conversion_output.value == pytest.approx(133.3220, 0.0003)


def test_psi():
    x = q.Quantity(1, "psi")
    conversion_output = x.convert("Pa")
    assert conversion_output.value == pytest.approx(6894.757, 0.0002)


def test_atm():
    x = q.Quantity(1, "atm")
    conversion_output = x.convert("Pa")
    assert conversion_output.value == pytest.approx(101325.0)


def test_mole_con_henry_const():
    x = q.Quantity(1, "atm m^3 kg mol^-1")
    conversion_output = x.convert("Pa m^3 kg mol^-1")
    assert conversion_output.value == pytest.approx(101325.0)


def test_pdl():
    x = q.Quantity(1, "pdl")
    conversion_output = x.convert("N")
    assert conversion_output.value == pytest.approx(0.13826, 0.0001)


def test_ozf():
    x = q.Quantity(1, "ozf")
    conversion_output = x.convert("N")
    assert conversion_output.value == pytest.approx(0.27802, 0.0001)


if __name__ == "__main__":
    v1 = q.Quantity(10.2, "m/s")  # Instantiation
    print(v1)
    print(v1.convert("cm/s"))  # conversion m/s to cm/s
    print(v1.convert("ft/s"))  # conversion m/s to ft/s
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
    print(a1.convert("cm/s^2"))  # conversion m/s^-2 to cm/s^-2
    print(a1.convert("ft/s^2"))  # conversion m/s^-2 to ft/s^-2

    print("\n angle \n")
    d1 = q.Quantity(1, "deg")
    r1 = q.Quantity(1, "rad")
    print(d1)
    print(r1)
    print(d1.convert("rad"))  # conversion deg to rad
    print(r1.convert("deg"))  # conversion rad to deg

    print("\n angluar-velocity \n")
    degps = q.Quantity(1, "deg/s")
    radps = q.Quantity(1, "rad/s")
    revpm = q.Quantity(1, "revolution/min")
    print(radps.convert("deg/s"))
    print(degps.convert("rad/s"))

    print("\n area \n")
    sq_m = q.Quantity(1, "m^2")
    print(sq_m)
    print(sq_m.convert("cm^2"))
    print(sq_m.convert("mm^2"))
    print(sq_m.convert("ft^2"))
    print(sq_m.convert("in^2"))

    print("\n area-inverse \n")
    in_sq_m = q.Quantity(1, "m^-2")
    print(in_sq_m)
    print(in_sq_m.convert("cm^-2"))
    print(in_sq_m.convert("mm^-2"))
    print(in_sq_m.convert("ft^-2"))
    print(in_sq_m.convert("in^-2"))

    print("\n collision-rate \n")
    cr = q.Quantity(1, "ft^-3 s^-1")
    print(cr)
    print(cr.convert("m^-3 s^-1"))

    print("\n temperature \n")
    tempC = q.Quantity(1, "degC")  # celsius
    print(tempC)
    print(tempC.convert("degK"))  # kelvin
    print(tempC.convert("degR"))  # rankine
    print(tempC.convert("degF"))  # fahrenheit

    print("\n youngs-modulus \n")
    ym = q.Quantity(1, "lbf ft^-2")
    print(ym)
    print(ym.convert("N m^-2"))

    ym2 = q.Quantity(1, "dyn cm^-2")
    print(ym2)
    print(ym2.convert("N m^-2"))

    print("\n volume \n")
    v = q.Quantity(1, "gal")
    print(v)
    print(v.convert("m^3"))

    print("\n viscosity \n")
    v = q.Quantity(1, "P")  # poise
    print(v)
    print(v.convert("kg m^-1 s^-1"))
