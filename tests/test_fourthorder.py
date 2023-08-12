import pytest
import sympy

from tensorconvert import FourthOrderTensor


@pytest.mark.parametrize("dim", [2, 3])
def test_conversion(dim):
    n = 6 if dim == 3 else 3

    a_voigt = sympy.randMatrix(n, n)
    a_voigt = a_voigt + a_voigt.T
    a = FourthOrderTensor(dim).from_voigt(a_voigt).as_array()
    assert FourthOrderTensor(dim).from_array(a).as_voigt() == a_voigt

    a_mandel = sympy.randMatrix(n, n)
    a_mandel = a_mandel + a_mandel.T
    a = FourthOrderTensor(dim).from_mandel(a_mandel).as_array()
    assert FourthOrderTensor(dim).from_array(a).as_mandel() == a_mandel

    n = 9 if dim == 3 else 4
    a_unsym = sympy.randMatrix(n, n)
    a = FourthOrderTensor(dim, symmetry=None).from_unsym(a_unsym).as_array()
    assert FourthOrderTensor(dim, symmetry=None).from_array(a).as_unsym() == a_unsym


@pytest.mark.parametrize("dim", [2, 3])
def test_operators(dim):
    def identity(x):
        return x

    a = FourthOrderTensor(dim).from_operator(identity)

    n = 6 if dim == 3 else 3
    assert FourthOrderTensor(dim).from_operator(identity).as_mandel() == sympy.eye(n)

    def linear_elastic(eps):
        lmbda, mu = sympy.symbols("lambda, mu", positive=True)
        return lmbda * sympy.trace(eps) * sympy.eye(dim) + 2 * mu * eps

    a = FourthOrderTensor(dim).from_operator(linear_elastic)

    assert FourthOrderTensor(dim).from_mandel(a.as_mandel()).as_voigt() == a.as_voigt()
    assert FourthOrderTensor(dim).from_voigt(a.as_voigt()).as_mandel() == a.as_mandel()
