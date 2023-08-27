# Conversion between tensor representations

```{toctree}
:hidden: true
:maxdepth: 1

api
notebooks/second-order
notebooks/fourth-order
```

## Introduction

Second-order and fourth-order tensors admit various matrix representations as explained in [Helnwein, P. (2001)](https://doi.org/10.1016/S0045-7825(00)00263-2). Once a basis has been chosen for the space of (symmetric) second-order tensors, they can be represented respectively by *vectors* and *matrices*. The choice of such basis depends on the physical and numerical problem at hand, and can also be influenced by computer implementation. Conversion between different representations may hence become necessary.

Although the scope of this package is not limited to continuum mechanics, many of the provided representations originate from it. If they do not suit your particular application, please feel free to [open an issue](https://github.com/tianyikillua/tensorconvert/issues) on the [GitHub page](https://github.com/tianyikillua/tensorconvert).

## API

The easy-to-use API is inspired from [scipy.spatial.transform.Rotation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html):

- Representing an existing tensor is performed by `as_...` methods.
- Initializing from a representation uses `from_...` methods.

Thanks to the [Fluent API](https://en.wikipedia.org/wiki/Fluent_interface#Python), `as_...` methods can be applied directly after `from_...` methods. For example, to convert a fourth-order tensor represented by Mandel notation to Voigt notation, we can do

```python
FourthOrderTensor(...).from_mandel(...).to_voigt()
```

For a detailed overview of API, please [read the API documentation](api).

## Examples

Tutorials and examples of using this package can be found in two notebooks. It is recommended to read the [notebook for second-order tensors](notebooks/second-order) first, before [that for fourth-order tensors](notebooks/fourth-order).

For [second-order tensors](notebooks/second-order), the following vector representations are available

- Voigt notation for strain-like quantities
- Voigt notation for stress-like quantities
- Mandel notation
- Unsymmetric notation

[Fourth-order tensors](notebooks/fourth-order) can be written using the following matrix representations

- Voigt notation
- Mandel notation
- Unsymmetric notation
