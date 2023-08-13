import itertools

import pytest
import sympy

from tensorconvert import SecondOrderTensor

dim = [2, 3]
ordering = ["121323", "122313", "231312"]


@pytest.mark.parametrize("dim, ordering", itertools.product(dim, ordering))
def test_conversion(dim, ordering):
    array = sympy.randMatrix(dim, dim)
    array += array.T
    a = SecondOrderTensor(dim, ordering).from_array(array)
    for basis in ["mandel", "voigt_strain", "voigt_stress", "unsym"]:
        assert (
            getattr(a, "from_" + basis)(getattr(a, "as_" + basis)()).as_array() == array
        )
