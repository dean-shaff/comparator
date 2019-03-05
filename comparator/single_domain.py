import typing

import numpy as np
import scipy.signal

from .trackable_dict import TrackableDict

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
        self._operators = TrackableDict({})
        self._products = TrackableDict({})
        self._representations = TrackableDict({
            "cartesian": (np.real, np.imag),
            "polar": (np.abs, np.angle)
        })
        self._current_representation = "cartesian"

    def __call__(self, *arrays: typing.Tuple[np.ndarray]) -> list:

        arrays = self.transform(*arrays)
        n_arrays = len(arrays)
        iscomplex = np.iscomplexobj(arrays[0])
        if iscomplex:
            rep = self._representations[self._current_representation]
        else:
            rep = (lambda a: a, )
        res = [[] for arr in arrays]
        for i in range(n_arrays):
            for j in range(n_arrays):
                if i > j:
                    continue
                elif i == j:
                    a = arrays[i]
                    for rep_fn in rep:
                        a_rep = rep_fn(a)
                        res[i].append(self.operate(a_rep))
                else:
                    a, b = arrays[i], arrays[j]
                    for rep_fn in rep:
                        a_rep, b_rep = rep_fn(a), rep_fn(b)
                        res[i].append(self.compare(a_rep, b_rep))

        return res

    def transform(self, *arrays: typing.Tuple[np.ndarray]) -> list:

        min_size = min([a.shape[0] for a in arrays])
        transformed = []
        for arr in arrays:
            arr = arr[:min_size][self._operation_domain]
            if self._transforms["forward"] is not None:
                transformed.append(self._transforms["forward"](arr))
            else:
                transformed.append(arr)

        return transformed

    def operate(self, a: np.ndarray) -> dict:
        res_dict = {}
        for prod_name in self._products:
            prod = self._products[prod_name]
            res_dict[prod_name] = prod(a)
        return res_dict

    def compare(self, a: np.ndarray, b: np.ndarray) -> dict:
        res_dict = {}
        for op_name in self._operators:
            res_dict[op_name] = []
            op = self._operators[op_name]
            res = op(a, b)
            res_dict[op_name].append(res)
            res_dict[op_name].append({})
            for prod_name in self._products:
                prod = self._products[prod_name]
                res_dict[op_name][1][prod_name] = prod(res)
        return res_dict

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
    def domain(self, arr: list):
        self._operation_domain = slice(*arr)


class TimeDomainComparator(SingleDomainComparator):

    def __init__(self, name="time"):
        super(TimeDomainComparator, self).__init__(name)

    def transform(self, *arrays: typing.Tuple[np.ndarray]) -> list:
        intermediate = super(TimeDomainComparator, self).transform(*arrays)
        transformed = [intermediate[0]]
        for arr in intermediate[1:]:
            transformed.append(self.time_align(transformed[0], arr)[-1])

        return transformed

    def time_align(self,
                   a: np.ndarray,
                   b: np.ndarray) -> typing.Tuple[np.ndarray]:
        """
        Align signal b with signal a in time.
        """
        a = a / np.amax(a)
        b = b / np.amax(b)
        xcorr = scipy.signal.fftconvolve(a, np.conj(b)[::-1], mode="full")
        mid_idx = int(xcorr.shape[0] // 2)
        max_arg = np.argmax(xcorr)
        offset = max_arg - mid_idx
        return a, np.roll(b, abs(offset))


class FrequencyDomainComparator(SingleDomainComparator):

    def __init__(self, name="frequency", fft_size=1024):
        super(FrequencyDomainComparator, self).__init__(
            name=name,
            forward_transform=np.fft.fft,
            inverse_transform=np.fft.ifft
        )
        self._operator_domain = slice(0, fft_size)
