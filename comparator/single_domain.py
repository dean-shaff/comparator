import typing
import logging
import inspect
import functools

import numpy as np
import scipy.signal

from .trackable import TrackableDict
from .product_result import ComparatorProductResult
from .operator_result import ComparatorOperatorResult

vector_function = typing.Callable[[np.ndarray], np.ndarray]
domain_type = typing.Union[slice, list, tuple]

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
        self._operation_domain = lambda size: slice(0, None)  # get whole array
        self._operators = TrackableDict({})
        self._products = TrackableDict({})

    def __call__(self,
                 *arrays: typing.Tuple[np.ndarray],
                 labels=None) -> typing.Tuple[list]:
        module_logger.debug(
            f"SingleDomainComparator.__call__: len(arrays): {len(arrays)}")
        arrays = self.transform(*arrays)
        res_op = {}
        res_prod = {}
        for op_name in self._operators:
            op = self._operators[op_name]
            _res_op, _res_prod = self.get_operator_products(op, arrays)
            res_op[op_name] = ComparatorOperatorResult(
                result=_res_op, labels=labels, name=op_name)
            res_prod[op_name] = ComparatorProductResult(
                products=_res_prod, labels=labels)

        return res_op, res_prod

    def transform(self, *arrays: typing.Tuple[np.ndarray]) -> list:
        module_logger.debug(
            f"SingleDomainComparator.transform")
        min_size = min([a.shape[0] for a in arrays])
        transformed = []
        for arr in arrays:
            arr = arr[:min_size][self._operation_domain(min_size)]
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
        """
        Apply an operator to arrays. Get products from the result of the
        operator.
        """
        res_op = []
        res_prod = []

        def _get_operator_products(op, arrays, res_op, res_prod):
            for arr in arrays:
                sig_op = inspect.signature(op)
                if len(sig_op.parameters) > 1:
                    res_op.append([])
                    res_prod.append([])
                    new_op = functools.partial(op, arr)
                    _get_operator_products(
                        new_op, arrays, res_op[-1], res_prod[-1])
                else:
                    res_op.append(op(arr))
                    res_prod.append(self.get_products(res_op[-1]))

        _get_operator_products(
            op, arrays, res_op, res_prod)

        return res_op, res_prod

    def get_products(self, a: np.ndarray) -> dict:
        res_prod = {}
        for prod_name in self._products:
            prod = self._products[prod_name]
            res_prod[prod_name] = prod(a)
        return res_prod

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
    def domain(self, new_domain: domain_type):
        if hasattr(new_domain, "__iter__"):  # means we're passing a list
            if any([isinstance(v, float) for v in new_domain]):
                self._operation_domain = \
                    lambda a: slice(*[int(v*a) for v in new_domain])
            else:
                self._operation_domain = lambda a: slice(*new_domain)
        elif hasattr(new_domain, 'start'):  # means we're passing a slice
            self._operation_domain = lambda a: new_domain
        elif callable(new_domain):
            self._operation_domain = new_domain


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
        a = a / np.amax(np.abs(a))
        b = b / np.amax(np.abs(b))
        xcorr = scipy.signal.fftconvolve(a, np.conj(b)[::-1], mode="full")
        mid_idx = int(xcorr.shape[0] // 2)
        max_arg = np.argmax(xcorr)
        offset = max_arg - mid_idx
        return offset
        # return a, np.roll(b, abs(offset))


class FrequencyDomainComparator(SingleDomainComparator):

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
