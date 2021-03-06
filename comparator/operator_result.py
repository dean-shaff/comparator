import logging

__all__ = [
    "ComparatorOperatorResult"
]

module_logger = logging.getLogger(__name__)


class ComparatorOperatorResult:
    """
    A convenient represention for the data returned
    by calling operators on data in a SingleDomainComparator object.
    """
    def __init__(self, result=None, labels=None, name=None):
        if result is None:
            result = []
        self._result = result
        self._labels = labels
        self._name = name

    def __getitem__(self, item):
        """
        Examples:

        .. code-block:: python
            >>> np.iscomplexobj(input_data[0])
            True
            >>> comp.operators["this"] = lambda a: a
            >>> res_op, res_prod = comp.cartesian(*input_data,
                                        labels=["one", "two", "three"])
            >>> res_op["this"]["one"]  # first element of input_data
            >>> res_op[0]  # first element of input_data
            >>> res_op[0, 0, 0]  # first value of first element of real
                                 # component of input_data

        Args:
            item (str, tuple, int): Item we which to retrieve from result
        Returns:
            list, np.ndarray, or number
        """
        if hasattr(item, "format"):  # str object
            if self._labels is not None:
                if item in self._labels:
                    idx = self._labels.index(item)
                    return self.__getitem__(idx)
            msg = ("ComparatorOperatorResult.__getitem__: "
                   f"cannot find {item} in labels")
            module_logger.error(msg)
            raise RuntimeError(msg)

        elif hasattr(item, "index"):  # tuple object
            res = self._result[item[0]]
            for i in item[1:]:
                if hasattr(res, "__getitem__"):
                    res = res[i]
                else:
                    break
            return res
        else:
            return self._result[item]

    def __iter__(self):
        return self._result.__iter__()

    def __len__(self):
        return len(self._result)

    def __str__(self):
        if self.labels is None:
            return self._result.__str__()
        else:
            res_str = []
            for label in self.labels:
                res_str.append(label)
                res_str.append("\n")
                res_str.append(self[label].__str__())
            return "".join(res_str)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, labels):
        msg = None
        if labels is None:
            self._labels = labels
        elif hasattr(labels, "__iter__") and not hasattr(labels, "format"):
            if len(labels) == len(self):
                self._labels = labels
            else:
                msg = (f"OperatorResult.labels: "
                       f"Can't set labels attribute with {labels}: "
                       f"Not enough elements")
        else:
            msg = (f"OperatorResult.labels: "
                   f"Can't set labels attribute with {labels}: "
                   f"labels needs to be list or tuple")

        if msg is not None:
            module_logger.error(msg)
            raise RuntimeError(msg)

    @property
    def result(self):
        return self._result
