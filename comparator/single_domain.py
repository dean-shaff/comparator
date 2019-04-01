import typing
import logging
import inspect
import functools

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
        self._accumulator = lambda a: a
        self._representations = TrackableDict({
            "cartesian": (np.real, np.imag),
            "polar": (np.abs, np.angle)
        })
        self._current_representation = "cartesian"
        self._accumulate_op = []
        self._accumulate_prod = []

    def __call__(self,
                 *arrays: typing.Tuple[np.ndarray]) -> typing.Tuple[list]:
        module_logger.debug(
            f"SingleDomainComparator.__call__: len(arrays): {len(arrays)}")
        arrays = self.transform(*arrays)
        res_op = {}
        res_prod = {}
        for op_name in self._operators:
            op = self._operators[op_name]
            _res_op, _res_prod = self.get_operator_products(op, arrays)
            res_op[op_name] = _res_op
            res_prod[op_name] = ComparatorProductResult(_res_prod)

        return res_op, res_prod

    def accumulate(self,
                   *arrays: typing.Tuple[np.ndarray]) -> typing.Tuple[list]:
        module_logger.debug(
            f"SingleDomainComparator.accumulate")
        res_op, res_prod = self.__call__(*arrays)
        self._accumulate_op.append(res_op)
        self._accumulate_prod.append(res_prod)

        return self._accumulate_op, self._accumulate_prod

    def transform(self, *arrays: typing.Tuple[np.ndarray]) -> list:
        module_logger.debug(
            f"SingleDomainComparator.transform")
        min_size = min([a.shape[0] for a in arrays])
        transformed = []
        for arr in arrays:
            arr = arr[:min_size][self._operation_domain]
            if self._transforms["forward"] is not None:
                transformed.append(self._transforms["forward"](arr))
            else:
                transformed.append(arr)

        return transformed

    def get_operator_products(
        self,
        op: typing.Callable,
        arrays: typing.Tuple[np.ndarray]
    ) -> typing.Tuple[list]:

        res_op = []
        res_prod = []
        iscomplex = np.iscomplexobj(arrays[0])
        if iscomplex:
            rep = self._representations[self._current_representation]
        else:
            rep = (lambda a: a, )
        n_rep = len(rep)

        def _get_operator_products(ops, arrays, res_op, res_prod):
            for arr in arrays:
                # new_op = functools.partial(op, arr)
                sig_op = inspect.signature(ops[0])
                if len(sig_op.parameters) > 1:
                    res_op.append([])
                    res_prod.append([])
                    new_ops = [functools.partial(ops[j], rep[j](arr))
                               for j in range(n_rep)]
                    _get_operator_products(
                        new_ops, arrays, res_op[-1], res_prod[-1])
                else:
                    res_op.append([ops[j](rep[j](arr)) for j in range(n_rep)])
                    res_prod.append([self.get_products(a) for a in res_op[-1]])

        _get_operator_products(
            [op for i in range(n_rep)], arrays, res_op, res_prod)
        return res_op, res_prod

    def get_products(self, a: np.ndarray) -> dict:
        res_prod = {}
        for prod_name in self._products:
            prod = self._products[prod_name]
            res_prod[prod_name] = prod(a)
        return res_prod

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
    def accumulator(self):
        return self._accumulator

    @property
    def domain(self):
        return self._operation_domain

    @domain.setter
    def domain(self, arr: list):
        self._operation_domain = slice(*arr)

    @property
    def accumulate_prod(self):
        return self.accumulate_prod

    @property
    def accumulate_op(self):
        return self._accumulate_op


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
