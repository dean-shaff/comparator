import typing

import numpy as np

vector_function = typing.Callable[[np.ndarray], np.ndarray]


class SingleDomainComparator:

    def __init__(self, name: str,
                 forward_transform: vector_function = None,
                 inverse_transform: vector_function = None):
        self._name = name
        self._transforms = {
            "forward": forward_transform,
            "inverse": inverse_transform
        }
        self._operation_domain = slice(0, None)  # get whole array
        self._operators = {}
        self._products = {}
        self._representations = {
            "cartesian": (np.real, np.imag),
            "polar": (np.abs, np.angle)
        }
        self._current_representation = "cartesian"

    def __call__(self, *arrays: typing.Tuple[np.ndarray]) -> list:

        arrays = self._transform(*arrays)
        n_arrays = len(arrays)
        iscomplex = np.iscomplexobj(arrays[0])
        if iscomplex:
            rep = self._representations[self._current_representation]
        else:
            rep = (lambda a: a)
        res = []
        for i in range(n_arrays - 1):
            for j in range(n_arrays - 1):
                if i == j or i > j:
                    continue
                else:
                    a, b = arrays[i], arrays[j]
                    for rep_fn in rep:
                        a_rep, b_rep = rep_fn(a), rep_fn(b)
                        res.append(self._operate(a_rep, b_rep))

        return res

    def _transform(self, *arrays: typing.Tuple[np.ndarray]) -> list:

        min_size = min([a.shape[0] for a in arrays])
        transformed = []
        for arr in transformed:
            arr = arr[:min_size][self._operation_domain]
            if self._transforms["forward"] is not None:
                transformed.append(self._transforms["forward"](arr))
            else:
                transformed.append(arr)

        return transformed

    def _operate(self, a: np.ndarray, b: np.ndarray) -> dict:
        res = {}
        for op_name in self._operators:
            res[op_name] = []
            op = self._operators[op_name]
            res = op(a, b)
            res[op_name].append(res)
            res[op_name].append({})
            for prod_name in self._products:
                prod = self._products[prod_name]
                res[op_name][prod_name] = prod(res)
        return res

    def __getattr__(self, attr: str):
        if attr in self._representations:
            self._current_representation = attr
            return self

    @property
    def name(self):
        return self._name

    @property
    def operators(self):
        return self._operators

    @property
    def products(self):
        return self._products

    @property
    def domain(self):
        return self._operation_domain

    @domain.setter
    def domain(self, arr):
        self._operation_domain = slice(*arr)
