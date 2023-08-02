import sympy
from tensorconvertor import SecondOrderTensor


def test_array():
    a_voigt = sympy.randMatrix(6, 1)
    a = SecondOrderTensor().from_voigt_strain(a_voigt).as_array()
    assert SecondOrderTensor().from_array(a).as_voigt_strain() == a_voigt

    a_mandel = sympy.randMatrix(6, 1)
    a = SecondOrderTensor().from_mandel(a_mandel).as_array()
    assert SecondOrderTensor().from_array(a).as_mandel() == a_mandel
