from pytest import approx

import ansys.fluent.core.quantity as q


def test_viscosity():
    v = q.Quantity(1, "P")  # poise
    conversion_output = v["kg m^-1 s^-1"]
    assert conversion_output._real_value == 0.1


def test_volume():
    v = q.Quantity(1, "gal")
    conversion_output = v["m^3"]
    assert conversion_output._real_value == approx(0.00378541)


def test_youngs_modulus():
    ym = q.Quantity(1, "lbf ft^-2")
    conversion_output = ym["N m^-2"]
    assert conversion_output._real_value == approx(47.89, 0.1)


def test_temperature():
    tempC = q.Quantity(1, "degC")  # celsius
    conversion_output_1 = tempC["degK"]
    assert conversion_output_1._real_value == 274.15
    conversion_output_2 = tempC["degR"]
    assert conversion_output_2._real_value == approx(493.46, 0.1)
    conversion_output_3 = tempC["degF"]
    assert conversion_output_3._real_value == approx(33.79, 0.1)


def test_collision_rate():
    cr = q.Quantity(1, "ft^-3 s^-1")
    conversion_output = cr["m^-3 s^-1"]
    assert conversion_output._real_value == approx(35.3147, 0.001)


def test_area_inverse():
    in_sq_m = q.Quantity(1, "m^-2")
    conversion_output = in_sq_m["cm^-2"]
    assert conversion_output._real_value == approx(0.0001)


def test_area():
    in_sq_m = q.Quantity(1, "m^2")
    conversion_output = in_sq_m["in^2"]
    assert conversion_output._real_value == approx(1550, 0.1)


def test_angular_velocity():
    degps = q.Quantity(1, "deg/s")
    conversion_output = degps["rad/s"]
    assert conversion_output._real_value == approx(0.01745, 0.001)


if __name__ == "__main__":
    v1 = q.Quantity(10.2, "m/s")  # Instantiation
    print(v1)
    print(v1["cm/s"])  # conversion m/s to cm/s
    print(v1["ft/s"])  # conversion m/s to ft/s
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
    print(a1["cm/s^2"])  # conversion m/s^-2 to cm/s^-2
    print(a1["ft/s^2"])  # conversion m/s^-2 to ft/s^-2

    print("\n angle \n")
    d1 = q.Quantity(1, "deg")
    r1 = q.Quantity(1, "rad")
    print(d1)
    print(r1)
    print(d1["rad"])  # conversion deg to rad
    print(r1["deg"])  # conversion rad to deg

    print("\n angluar-velocity \n")
    degps = q.Quantity(1, "deg/s")
    radps = q.Quantity(1, "rad/s")
    revpm = q.Quantity(1, "revolution/min")
    print(radps["deg/s"])
    print(degps["rad/s"])

    print("\n area \n")
    sq_m = q.Quantity(1, "m^2")
    print(sq_m)
    print(sq_m["cm^2"])
    print(sq_m["mm^2"])
    print(sq_m["ft^2"])
    print(sq_m["in^2"])

    print("\n area-inverse \n")
    in_sq_m = q.Quantity(1, "m^-2")
    print(in_sq_m)
    print(in_sq_m["cm^-2"])
    print(in_sq_m["mm^-2"])
    print(in_sq_m["ft^-2"])
    print(in_sq_m["in^-2"])

    print("\n collision-rate \n")
    cr = q.Quantity(1, "ft^-3 s^-1")
    print(cr)
    print(cr["m^-3 s^-1"])

    print("\n temperature \n")
    tempC = q.Quantity(1, "degC")  # celsius
    print(tempC)
    print(tempC["degK"])  # kelvin
    print(tempC["degR"])  # rankine
    print(tempC["degF"])  # fahrenheit

    print("\n youngs-modulus \n")
    ym = q.Quantity(1, "lbf ft^-2")
    print(ym)
    print(ym["N m^-2"])

    ym2 = q.Quantity(1, "dyn cm^-2")
    print(ym2)
    print(ym2["N m^-2"])

    print("\n volume \n")
    v = q.Quantity(1, "gal")
    print(v)
    print(v["m^3"])

    print("\n viscosity \n")
    v = q.Quantity(1, "P")  # poise
    print(v)
    print(v["kg m^-1 s^-1"])
