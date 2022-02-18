import numbers

import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin


def v_scalar_prod(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])


def v_scalar_prod(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])


class MyMatrix:
    def __init__(self, data):
        if isinstance(data, MyMatrix):
            self._data = list(data._data)
            return
        if not isinstance(data, list) or not all(isinstance(r, list) for r in data):
            raise ValueError('Invalid data format')
        self.shape = (len(data), len(data[0]))
        if not all(len(r) == self.shape[1] for r in data):
            raise ValueError('Invalid matrix shape')
        self._data = data

    def __repr__(self):
        repr = []
        for r in self._data:
            repr.append(', '.join(map(str, r)))
        return '[[' + ']\n['.join(repr) + ']]'

    def check_correct_arg(self, other, matmul=False):
        if not isinstance(other, MyMatrix):
            raise ValueError('Second argument is not a MyMatrix')
        if not matmul and self.shape != other.shape:
            raise ValueError('Invalid matrix dimentions', self.shape, other.shape)
        if matmul and self.shape[1] != other.shape[0]:
            raise ValueError('Invalid matrix dimentions', self.shape, other.shape)

    def __add__(self, other):
        self.check_correct_arg(other)
        result = []
        for i in range(self.shape[0]):
            r = []
            for j in range(self.shape[1]):
                r.append(self._data[i][j] + other._data[i][j])
            result.append(r)
        return MyMatrix(result)

    def __mul__(self, other):
        self.check_correct_arg(other)
        result = []
        for i in range(self.shape[0]):
            r = []
            for j in range(self.shape[1]):
                r.append(self._data[i][j] * other._data[i][j])
            result.append(r)
        return MyMatrix(result)

    def __matmul__(self, other):
        self.check_correct_arg(other, matmul=True)

        result = []
        for i in range(self.shape[0]):
            r = []
            for j in range(self.shape[1]):
                r.append(v_scalar_prod(self._data[i], [other._data[k][j] for k in range(other.shape[0])]))
            result.append(r)
        return MyMatrix(result)


class HashableMixin:
    def __hash__(self):
        # Hash of the matrix is a xor of all elements' hashes
        result = None
        for r in self._data:
            for v in r:
                if result is None:
                    result = hash(v)
                else:
                    result ^= hash(v)
        return result


class HashableMatrix(MyMatrix, HashableMixin):
    _mul_hashes = {}

    def __matmul__(self, other):
        self.check_correct_arg(other, matmul=True)

        hs = (hash(self), hash(other))

        if hs not in self._mul_hashes:
            self._mul_hashes[hs] = HashableMatrix(super(HashableMatrix, self).__matmul__(other))
        return self._mul_hashes[hs]


class ExpandedMatrix:
    def __repr__(self):
        repr = []
        for r in self.value:
            repr.append(', '.join(map(str, r)))
        return '[[' + ']\n['.join(repr) + ']]'

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self))

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = np.asarray(new_value)


class MixinMatrix(NDArrayOperatorsMixin, ExpandedMatrix):
    def __init__(self, value):
        self._value = np.asarray(value)

    # One might also consider adding the built-in list type to this
    # list, to support operations like np.add(array_like, list)
    _HANDLED_TYPES = (np.ndarray, numbers.Number, list)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (MixinMatrix,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.value if isinstance(x, MixinMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, MixinMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
