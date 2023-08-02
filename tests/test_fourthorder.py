import sympy
from tensorconvertor import FourthOrderTensor


def test_array():
    a_voigt = sympy.randMatrix(6)
    a_voigt = a_voigt + a_voigt.T
    a = FourthOrderTensor().from_voigt(a_voigt).as_array()
    assert FourthOrderTensor().from_array(a).as_voigt() == a_voigt

    a_mandel = sympy.randMatrix(6)
    a_mandel = a_mandel + a_mandel.T
    a = FourthOrderTensor().from_mandel(a_mandel).as_array()
    assert FourthOrderTensor().from_array(a).as_mandel() == a_mandel

    a_unsym = sympy.randMatrix(9)
    a = FourthOrderTensor(symmetry=None).from_unsym(a_unsym).as_array()
    FourthOrderTensor(symmetry=None).from_array(a).as_unsym() == a_unsym


def test_identity():
    def identity(x):
        return x

    assert FourthOrderTensor().from_operator(identity).as_mandel() == sympy.eye(6)
    assert FourthOrderTensor(dim=2).from_operator(identity).as_mandel() == sympy.eye(3)

    def linear_elastic(eps, dim=3):
        lmbda, mu = sympy.symbols("lambda, mu", positive=True)
        return lmbda * sympy.trace(eps) * sympy.eye(dim) + 2 * mu * eps

    assert (
        FourthOrderTensor()
        .from_mandel(FourthOrderTensor().from_operator(linear_elastic).as_mandel())
        .as_voigt()
        == FourthOrderTensor().from_operator(linear_elastic).as_voigt()
    )
    assert (
        FourthOrderTensor()
        .from_voigt(FourthOrderTensor().from_operator(linear_elastic).as_voigt())
        .as_mandel()
        == FourthOrderTensor().from_operator(linear_elastic).as_mandel()
    )
