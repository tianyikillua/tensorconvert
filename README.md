# Conversion between tensor representations

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GitHub](https://img.shields.io/github/license/tianyikillua/tensorconvert)](https://github.com/tianyikillua/tensorconvert/blob/master/LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation](https://readthedocs.org/projects/tensorconvert/badge/?version=latest)](https://tensorconvert.readthedocs.io/en/latest/)

This package provides an easy-to-use API to represent **symbolic** second-order and fourth-order tensors. Various representations frequently used in physics are provided and conversion between them can be obtained.

Compared to [mechkit](https://github.com/JulianKarlBauer/mechkit), the scope of this package is not limited to continuum mechanics since these representations can be used for other domains.

The API is inspired from [scipy.spatial.transform.Rotation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html):

- Representing an existing tensor is performed by `as_...` methods.
- Initializing from a representation uses `from_...` methods.

Thanks to the [Fluent API](https://en.wikipedia.org/wiki/Fluent_interface#Python), `as_...` methods can be applied directly after `from_...` methods. For example, to convert a fourth-order tensor represented by Mandel notation to Voigt notation, we can do
```python
FourthOrderTensor(...).from_mandel(...).to_voigt()
```

## Installation

[sympy](https://www.sympy.org/) is a strong dependency of this package since all tensor representations are `sympy` objects.

The package is still being developed. You can use `pip` to install the current `main` version.
```sh
pip install -U git+https://github.com/tianyikillua/tensorconvert.git@main
```

## Documentation

Refer to the [documentation](https://tensorconvert.readthedocs.io/en/latest/) for the API and the examples using `tensorconvert`.
