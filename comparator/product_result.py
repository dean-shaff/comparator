import typing

__all__ = [
    "ComparatorProductResult"
]


class ComparatorProductResult:
    """
    This class represents the data returned from
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
        if hasattr(products[0], "keys"):
            return list(products[0].keys())
        else:
            return self.get_product_names(products[0])

    def __getitem__(self, item: typing.Any):
        if hasattr(item, "split"):  # str like
            res = []
            complex_dim = self.complex_dim  # requires a calculation everytime

            def _get_item(products, res):
                if products is None:
                    res.append(None)
                elif hasattr(products[0], "keys"):
                    sub_item = [{item: products[z][item]}
                                for z in range(complex_dim)]
                    res.append(sub_item)
                else:
                    res.append([])
                    for i in range(len(self)):
                        _get_item(products[i], res[-1])

            _get_item(self._products, res)
            return ComparatorProductResult(res[0])
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

        item = self._product_names[0]
        complex_dim = self.complex_dim

        def single_row(row):
            # print(row)
            return [[row[j][z][item]
                    for z in range(complex_dim)]
                    if row[j] is not None else None
                    for j in range(len(row))]

        def _iter(products):
            if products[0] is None:
                yield single_row(products)
            elif hasattr(products[0][0], "keys"):
                yield single_row(products)
            else:
                for i in range(len(self)):
                    for val in _iter(products[i]):
                        yield val

        if len(self._product_names) == 1:
            # this is the base case of single dimensional data
            if hasattr(self._products[0][0], "keys"):
                for val in single_row(self._products):
                    yield val
            # higher dimensional data gets passed to _iter
            else:
                for val in _iter(self._products):
                    yield val

        else:
            raise ValueError(("__iter__ is ill defined for "
                              "ComparatorProductResult object "
                              "with multiple products"))

    def __len__(self) -> int:
        return len(self._products)

    def __contains__(self, item) -> bool:
        if item in self._product_names:
            return True
        else:
            return False

    def __format__(self, format_spec: str) -> str:
        self._format_spec = format_spec
        return str(self)

    def __str__(self) -> str:

        complex_dim = self.complex_dim
        len_self = len(self)

        res = {name: [] for name in self._product_names}

        def _iter(product):
            if hasattr(product[0][0], "keys"):
                for name in self._product_names:
                    res[name].append(
                        ", ".join(
                            ["".join(["[", ",".join(
                                [f'{product[j][z][name]:{self._format_spec}}'
                                 for z in range(complex_dim)]
                              ), "]"])
                             for j in range(len_self)]
                        )
                    )
                    res[name].append("\n")
            else:
                for i in range(len_self):
                    _iter(product[i])

        _iter(self._products)

        res_str = []
        for name in self._product_names:
            res_str.append(name)
            res_str.append("\n")
            res_str.append("".join(res[name]))
        res_str = "".join(res_str)
        return res_str

    @property
    def products(self) -> list:
        return self._products

    @property
    def complex_dim(self) -> int:

        def _get_complex_dim(products):
            if hasattr(products[0], "keys"):
                return len(products)
            else:
                return _get_complex_dim(products[0])

        return _get_complex_dim(self._products)

    @property
    def iscomplex(self) -> bool:
        return True if self.complex_dim == 2 else False

    @property
    def isreal(self) -> bool:
        return not self.iscomplex
