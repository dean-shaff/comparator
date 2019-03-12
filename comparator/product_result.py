__all__ = [
    "ComparatorProductResult"
]


class ComparatorProductResult:

    def __init__(self, products: list = None):

        if products is None:
            products = []
            product_names = []
        else:
            product_names = list(products[0][0][0].keys())
        self._products = products
        self._product_names = product_names

    def __getitem__(self, item):
        if hasattr(item, "split"):  # str like
            res = [[[{item: self._products[i][j][z][item]}
                     for z in range(self.complex_dim)]
                    if self._products[i][j] is not None else None
                   for j in range(len(self))]
                   for i in range(len(self))]
            return ComparatorProductResult(res)
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
        if len(self._product_names) == 1:
            item = self._product_names[0]
            for i in range(len(self)):
                sub_product = self._products[i]
                yield [[sub_product[j][z][item]
                        for z in range(self.complex_dim)]
                       if sub_product[j] is not None else None
                       for j in range(len(self))]
        else:
            raise ValueError(("__iter__ is ill defined for "
                              "ComparatorProductResult object "
                              "with multiple products"))

    def __len__(self) -> int:
        return len(self._products[0])

    def __contains__(self, item) -> bool:
        if item in self._product_names:
            return True
        else:
            return False

    # def __str__(self):
    #     res = []
    #     for name in self._product_names:
    #         prod_res = self.__getitem__(name)
    #         for i in range(len(self)):
    #             row = []
    #             for j in range(len(self)):
    #                 sub = prod_res[j][i]
    #                 if sub is not None:
    #                     row.append("[{}]".format(
    #                         ", ".join(["{:.6e}".format(sub[z])
    #                                    for z in range(self.complex_dim)])
    #                     ))
    #             res.append(" ".join(sub))

    @property
    def complex_dim(self) -> int:
        return len(self._products[0][0])

    @property
    def iscomplex(self) -> bool:
        complex_dim = len(self._products[0][0])
        return True if complex_dim == 2 else False

    @property
    def isreal(self) -> bool:
        return not self.iscomplex
