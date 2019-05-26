import logging
import typing

__all__ = [
    "ComparatorProductResult"
]

module_logger = logging.getLogger(__name__)


class ComparatorProductResult:
    """
    This class represents the products returned from each operator.

    A "product" can be any mapping from a vector to scalar, or tuple of
    scalars. For example, I could have a mean be something like the following:

    comp.products["mean"] = lambda a: (np.mean(a.real), np.mean(a.imag))

    We can access ComparatorProductResult using a variety of syntaxes:

    ..code-block:: python

        >>> product_result[0]["mean"] # get the mean of the first operator result
        >>> product_result["mean"]


    Internally, a ComparatorProductResult is a nest list of dictionaries.
    For a simple one to one operator, this looks pretty simple:


    ..code-block:: python

        >>> product_result = ComparatorProductResult(products=[
            {"mean": [0.5], "max": [1.0], "sum": [2.0]},
            {"mean": [0.4], "max": [1.0], "sum": [1.8]}
        ])

    For two to one operators, the representation is a nested list:

    ..code-block:: python

        >>> product_result = ComparatorProductResult(products=[
            [
                {"mean": [0.5], "max": [1.0], "sum": [2.0]},
                {"mean": [0.4], "max": [1.0], "sum": [1.8]}
            ],
            [
                {"mean": [0.5], "max": [1.0], "sum": [2.0]},
                {"mean": [0.4], "max": [1.0], "sum": [1.8]}
            ]
        ])



    """
    def __init__(self, products: list = None, labels: list = None):

        if products is None:
            products = []
            product_names = []
        else:
            product_names = self.get_product_names(products)

        self._products = products
        self._product_names = product_names
        self._format_spec = ".4f"
        self._labels = labels

    def get_product_names(self, products: list) -> list:
        module_logger.debug(
            f"ComparatorProductResult.get_product_names: products={products}")
        if hasattr(products, "keys"):
            return list(products.keys())
        else:
            return self.get_product_names(products[0])

    def __getitem__(self, item: typing.Any):
        if hasattr(item, "split"):  # str like
            res = []

            def _get_item(products, res):
                if products is None:
                    res.append(None)
                elif hasattr(products, "keys"):
                    res.append(products[item])
                else:
                    res.append([])
                    for i in range(len(self._products)):
                        _get_item(products[i], res[-1])

            _get_item(self._products, res)
            return res[0]
        elif hasattr(item, "index"):  # tuple object
            res = self._products[item[0]]
            for i in item[1:]:
                if res is None:
                    break
                res = res[i]
            return res
        else:
            return self._products[item]

    def __iter__(self):
        for name in self._product_names:
            yield (name, self[name])

    def __len__(self) -> int:
        return len(self._product_names)

    def __contains__(self, item) -> bool:
        if item in self._product_names:
            return True
        else:
            return False

    def __format__(self, format_spec: str) -> str:
        self._format_spec = format_spec
        return str(self)

    def __str__(self) -> str:

        def stringify(sub_product):
            res = []

            def _iter(sub_product):
                if hasattr(sub_product[0], "__iter__"):
                    res.append("[")
                    for l in sub_product[:-1]:
                        _iter(l)
                        res.append("\n")
                    _iter(sub_product[-1])
                    res.append("]\n")
                else:
                    res.append("".join(
                        ["[",
                            ", ".join(
                                [f"{val:{self._format_spec}}"
                                 for val in sub_product]
                            ),
                         "]"]
                    ))
            _iter(sub_product)
            return "".join(res)

        res_str = []
        for i, (key, val) in enumerate(self):
            res_str.append(key)
            res_str.append("\n")
            res_str.append(stringify(val))
            if i != len(self) - 1:
                res_str.append("\n")

        return "".join(res_str)

    @property
    def products(self) -> list:
        return self._products
