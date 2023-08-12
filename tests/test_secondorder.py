import pytest
import sympy

from tensorconvert import SecondOrderTensor


@pytest.mark.parametrize("dim", [2, 3])
def test_conversion(dim):
    array = sympy.randMatrix(dim, dim)
    array += array.T
    a = SecondOrderTensor(dim).from_array(array)
    for basis in ["mandel", "voigt_strain", "voigt_stress", "unsym"]:
        assert (
            getattr(a, "from_" + basis)(getattr(a, "as_" + basis)()).as_array() == array
        )
