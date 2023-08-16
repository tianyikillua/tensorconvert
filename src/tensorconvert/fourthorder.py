import sympy
from sympy.tensor.array.expressions import ArraySymbol
from .secondorder import SecondOrderTensor


class FourthOrderTensor:
    """Representations of fourth-order tensors

    Args:
        dim (int): Spatial dimension {2, 3}
        symmetry (str): Enforce symmetry for array {"major", "minor", None}
        ordering (str): Ordering of the off-diagonal components for 3-d tensors
            {"121323", "122313", "231312"}
    """

    def __init__(self, dim: int = 3, symmetry="major", ordering="121323"):
        self.second_order = SecondOrderTensor(dim, ordering)
        self.dim = dim
        self._ordering = self.second_order._ordering

        # Symmetry
        assert symmetry in ["major", "minor", None]
        self.symmetry = symmetry

        # Default tensor
        self.a = ArraySymbol("a", (self.dim,) * 4)

        # User-defined operator
        self.operator = None

    def _compute(self, x):
        assert x.shape == (self.dim, self.dim)

        if self.operator is not None:
            return self.operator(x)
        else:
            assert self.a is not None
            return self._compute_Ax(x)

    def _compute_Ax(self, x):
        y = sympy.zeros(self.dim, self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                for k in range(self.dim):
                    for l in range(self.dim):
                        y[i, j] = y[i, j] + self.a[i, j, k, l] * x[k, l]

        if self.symmetry in ["minor", "major"]:
            for i in range(self.dim):
                for j in range(self.dim):
                    for k in range(self.dim):
                        for l in range(k, self.dim):
                            y = y.subs(self.a[i, j, l, k], self.a[i, j, k, l])
            for k in range(self.dim):
                for l in range(self.dim):
                    for i in range(self.dim):
                        for j in range(i, self.dim):
                            y = y.subs(self.a[j, i, k, l], self.a[i, j, k, l])

        if self.symmetry == "major":
            ordering = self._ordering()
            for i in range(self.dim):
                for j in range(i, self.dim):
                    for k in range(self.dim):
                        for l in range(k, self.dim):
                            if ordering.index((i, j)) < ordering.index((k, l)):
                                y = y.subs(self.a[k, l, i, j], self.a[i, j, k, l])
        return y

    def as_operator(self):
        """Represent as linear operator on the second-order tensors"""
        return self._compute

    def as_array(self):
        """Represent as array"""
        if self.a is None:
            assert self.operator is not None
            mandel = self.as_mandel()
            self.from_mandel(mandel)
            self.operator = None
        return self.a

    def as_voigt(self):
        """Represent as Voigt notation"""
        basis = self.second_order.basis_voigt_strain()
        out = sympy.zeros(len(basis), len(basis))
        for i in range(len(basis)):
            y = self._compute(basis[i])
            out[:, i] = self.second_order.from_array(y).as_voigt_stress()
        out = sympy.simplify(out)
        return out

    def as_mandel(self):
        """Represent as Mandel notation"""
        basis = self.second_order.basis_mandel()
        out = sympy.zeros(len(basis), len(basis))
        for i in range(len(basis)):
            y = self._compute(basis[i])
            out[:, i] = self.second_order.from_array(y).as_mandel()
        out = sympy.simplify(out)
        return out

    def as_unsym(self):
        """Represent as the unsymmetric notation"""
        basis = self.second_order.basis_unsym()
        out = sympy.zeros(len(basis), len(basis))
        for i in range(len(basis)):
            y = self._compute(basis[i])
            out[:, i] = self.second_order.from_array(y).as_unsym()
        out = sympy.simplify(out)
        return out

    def from_operator(self, operator):
        """Initialize from linear operator on the second-order tensors"""
        self.a = None
        self.operator = operator
        return self

    def from_array(self, a):
        """Initialize from array"""
        assert a.shape == (self.dim,) * 4

        self.a = a
        self.operator = None
        return self

    def _from_basis(self, a, basis, symmetry=True):
        ordering = self._ordering(symmetry)
        assert a.shape == (len(ordering),) * 2

        self.a = None
        for i in range(len(ordering)):
            for j in range(len(ordering)):
                if self.a is None:
                    self.a = a[i, j] * basis[(i, j)]
                else:
                    self.a += a[i, j] * basis[(i, j)]
        return self

    def from_voigt(self, a):
        """Initialize from Voigt notation"""
        a_copy = sympy.Matrix(a)
        a_copy[:, self.dim :] *= sympy.sqrt(2)
        a_copy[self.dim :, :] *= sympy.sqrt(2)
        return self.from_mandel(a_copy)

    def from_mandel(self, a):
        """Initialize from Mandel notation"""
        return self._from_basis(a, self.basis_mandel())

    def from_unsym(self, a):
        """Initialize from the unsymmetric notation"""
        ordering = self._ordering(symmetry=False)
        assert a.shape == (len(ordering),) * 2

        self.a = sympy.Array.zeros(self.dim, self.dim, self.dim, self.dim).as_mutable()
        for oi in range(len(ordering)):
            i, j = ordering[oi]
            for oj in range(len(ordering)):
                k, l = ordering[oj]
                self.a[i, j, k, l] = a[oi, oj]
        return self

    def _basis(self, b):
        basis = {}
        for i in range(len(b)):
            for j in range(len(b)):
                basis[(i, j)] = sympy.tensorproduct(b[i], b[j])
        return basis

    def basis_mandel(self):
        """Basis vectors of Mandel notation"""
        return self._basis(self.second_order.basis_mandel())

    def basis_unsym(self):
        """Basis vectors of the unsymmetric notation"""
        return self._basis(self.second_order.basis_unsym())
