import typing
import copy
import logging

import numpy as np
import scipy.signal

from .trackable_dict import TrackableDict
from .product_result import ComparatorProductResult

vector_function = typing.Callable[[np.ndarray], np.ndarray]

__all__ = [
    "SingleDomainComparator",
    "TimeDomainComparator",
    "FrequencyDomainComparator"
]

module_logger = logging.getLogger(__name__)


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
        self._accumulate_op = []
        self._accumulate_prod = []

    def __call__(self,
                 *arrays: typing.Tuple[np.ndarray]) -> typing.Tuple[list]:

        arrays = self.transform(*arrays)
        n_arrays = len(arrays)
        iscomplex = np.iscomplexobj(arrays[0])
        if iscomplex:
            rep = self._representations[self._current_representation]
        else:
            rep = (lambda a: a, )
        res_op = {
            op_name: [[None for j in range(n_arrays)] for i in range(n_arrays)]
            for op_name in self._operators
        }
        res_prod = copy.deepcopy(res_op)
        for op_name in self._operators:
            for i in range(n_arrays):
                for j in range(n_arrays):
                    if i > j:
                        continue
                    res_op[op_name][i][j] = []
                    res_prod[op_name][i][j] = []
                    if i == j:
                        a = arrays[i]
                        for rep_fn in rep:
                            a_rep = rep_fn(a)
                            single_array_op = self.operate(a_rep)
                            res_op[op_name][i][j].append(single_array_op[0])
                            res_prod[op_name][i][j].append(single_array_op[1])
                    else:
                        a, b = arrays[i], arrays[j]
                        for rep_fn in rep:
                            a_rep, b_rep = rep_fn(a), rep_fn(b)
                            two_array_op = self.compare(a_rep, b_rep, op_name)
                            res_op[op_name][i][j].append(two_array_op[0])
                            res_prod[op_name][i][j].append(two_array_op[1])

        res_prod = {op_name: ComparatorProductResult(res_prod[op_name])}

        return res_op, res_prod

    def accumulate(self,
                   *arrays: typing.Tuple[np.ndarray]) -> typing.Tuple[list]:

        res_op, res_prod = self.__call__(*arrays)
        self._accumulate_op.append(res_op)
        self._accumulate_prod.append(res_prod)

        return self._accumulate_op, self._accumulate_prod

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

    def operate(self, a: np.ndarray) -> tuple:
        res_prod = {}
        for prod_name in self._products:
            prod = self._products[prod_name]
            res_prod[prod_name] = prod(a)
        return a, res_prod

    def compare(self, a: np.ndarray, b: np.ndarray, op_name: str) -> tuple:
        op = self._operators[op_name]
        res_op = op(a, b)
        res_prod = {}
        for prod_name in self._products:
            prod = self._products[prod_name]
            res_prod[prod_name] = prod(res_op)
        return res_op, res_prod

    # def laze(self, *args):
    #     """
    #     It could be that argu
    #     """

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
        transformed = [arrays[0]]
        for i, arr in enumerate(arrays[1:]):
            offset = self.get_time_delay(transformed[0], arr)
            module_logger.debug(
                (f"TimeDomainComparator.transform: "
                 f"offset for arr[{i}]: {offset}"))
            transformed.append(np.roll(arr, abs(offset)))
        return super(TimeDomainComparator, self).transform(*transformed)

    def get_time_delay(self,
                       a: np.ndarray,
                       b: np.ndarray) -> int:
        """
        Get the number of units of delay between a and b
        """
        a = a / np.amax(a)
        b = b / np.amax(b)
        xcorr = scipy.signal.fftconvolve(a, np.conj(b)[::-1], mode="full")
        mid_idx = int(xcorr.shape[0] // 2)
        max_arg = np.argmax(xcorr)
        offset = max_arg - mid_idx
        return offset
        # return a, np.roll(b, abs(offset))


class FrequencyDomainComparator(TimeDomainComparator):

    def __init__(self, name: str = "frequency", fft_size: int = 1024):
        super(FrequencyDomainComparator, self).__init__(
            name=name,
        )
        self._transforms = {
            "forward": np.fft.fft,
            "inverse": np.fft.ifft
        }
        self._operator_domain = slice(0, fft_size)

    def set_fft_size(self, fft_size: int):
        self._operator_domain = slice(0, fft_size)
