import sympy


class SecondOrderTensor:
    """Representations of second-order tensors.

    Args:
        dim (int): Spatial dimension {2, 3}
        ordering (str): Ordering of the off-diagonal components for 3-d tensors
            {"121323", "122313", "231312"}
    """

    def __init__(self, dim: int = 3, ordering="121323"):
        assert dim in [2, 3]
        self.dim = dim

        # Ordering
        assert ordering in ["121323", "122313", "231312"]
        self.ordering = ordering

        # Default tensor
        self.a = sympy.Matrix(sympy.MatrixSymbol("a", self.dim, self.dim))

    def as_array(self):
        """Represent as array"""
        return self.a

    def as_voigt_stress(self):
        """Represent using Voigt notation for stress"""
        ordering = self._ordering()
        stress = sympy.zeros(len(ordering), 1)
        for o in range(len(ordering)):
            i, j = ordering[o]
            stress[o] = self.a[i, j]
        return stress

    def as_voigt_strain(self):
        """Represent using Voigt notation for strain"""
        strain = self.as_voigt_stress()
        strain[self.dim :, :] *= 2
        return strain

    def as_mandel(self):
        """Represent using Mandel notation"""
        strain = self.as_voigt_stress()
        strain[self.dim :, :] *= sympy.sqrt(2)
        return strain

    def as_unsym(self):
        """Represent the unsymmetric notation"""
        ordering = self._ordering(symmetry=False)
        a = sympy.zeros(len(ordering), 1)
        for o in range(len(ordering)):
            i, j = ordering[o]
            a[o] = self.a[i, j]
        return a

    def from_array(self, a):
        """
        Initialize from matrix
        """
        assert a.shape == (self.dim, self.dim)

        self.a = a
        return self

    def from_voigt_stress(self, a):
        """Initialize from Voigt notation for stress"""
        ordering = self._ordering()
        assert a.shape == (len(ordering), 1)

        self.a = sympy.zeros(self.dim, self.dim)
        for o in range(len(ordering)):
            i, j = ordering[o]
            self.a[i, j] = a[o]
            if i != j:
                self.a[j, i] = self.a[i, j]
        return self

    def from_voigt_strain(self, a):
        """Initialize from Voigt notation for strain"""
        a_copy = a.copy()
        a_copy[self.dim :, :] /= 2
        return self.from_voigt_stress(a_copy)

    def from_mandel(self, a):
        """Initialize from Mandel notation"""
        a_copy = a.copy()
        a_copy[self.dim :, :] /= sympy.sqrt(2)
        return self.from_voigt_stress(a_copy)

    def from_unsym(self, a):
        """Initialize from the unsymmetric notation."""
        ordering = self._ordering(symmetry=False)
        assert a.shape == (len(ordering), 1)

        self.a = sympy.zeros(self.dim, self.dim)
        for o in range(len(ordering)):
            i, j = ordering[o]
            self.a[i, j] = a[o]
        return self

    def _basis(self, from_basis, symmetry):
        ordering = self._ordering(symmetry)
        eye = sympy.eye(len(ordering))
        basis = [from_basis(eye[:, i]).as_array() for i in range(len(ordering))]
        return basis

    def basis_voigt_stress(self):
        """Basis vectors of Voigt notation for stress"""
        return self._basis(self.from_voigt_stress, symmetry=True)

    def basis_voigt_strain(self):
        """Basis vectors of Voigt notation for strain"""
        return self._basis(self.from_voigt_strain, symmetry=True)

    def basis_mandel(self):
        """Basis vectors of Mandel notation"""
        return self._basis(self.from_mandel, symmetry=True)

    def basis_unsym(self):
        """Basis vectors of the unsymmetric notation"""
        return self._basis(self.from_unsym, symmetry=False)

    def _ordering(self, symmetry: bool = True):
        """Ordering of second-order tensor components"""
        if symmetry:
            if self.dim == 3:
                ordering = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]
                if self.ordering == "122313":
                    ordering = [ordering[i] for i in [0, 1, 2, 3, 5, 4]]
                elif self.ordering == "231312":
                    ordering = [ordering[i] for i in [0, 1, 2, 5, 4, 3]]
            else:
                ordering = [(0, 0), (1, 1), (0, 1)]
        else:
            if self.dim == 3:
                ordering = [
                    (0, 0),
                    (1, 1),
                    (2, 2),
                    (0, 1),
                    (1, 0),
                    (0, 2),
                    (2, 0),
                    (1, 2),
                    (2, 1),
                ]
                if self.ordering == "122313":
                    ordering = [ordering[i] for i in [0, 1, 2, 3, 4, 7, 8, 5, 6]]
                elif self.ordering == "231312":
                    ordering = [ordering[i] for i in [0, 1, 2, 7, 8, 5, 6, 3, 4]]
            else:
                ordering = [(0, 0), (1, 1), (0, 1), (1, 0)]
        return tuple(ordering)
