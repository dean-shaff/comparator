# multi_domain.py
from .single_domain import (
    SingleDomainComparator,
    FrequencyDomainComparator,
    TimeDomainComparator
)

__all__ = [
    "MultiDomainComparator",
    "TimeFreqDomainComparator"
]


class MultiDomainComparator(SingleDomainComparator):

    def __init__(self, name=None, domains=None):
        super(MultiDomainComparator, self).__init__(name)
        if domains is None:
            domains = {}
        self._domains = domains
        self._operators.on(self.on_change("operators"))
        self._products.on(self.on_change("products"))
        # self._operation_domain.on(self.on_change("domain"))

    def add_domain(self, *args: tuple, **kwargs: dict):
        if hasattr(args[0], "_name") and hasattr(args[0], "_transforms"):
            self._domains[args[0].name] = args[0]
        else:
            self._domains[args[0]] = SingleDomainComparator(*args, **kwargs)

    def on_change(self, name):

        def _on_change(*args):

            if len(args) == 2:
                # means we're setting
                item, val = args
                for domain_name in self._domains:
                    domain = self._domains[domain_name]
                    getattr(domain, name)[item] = val

            elif len(args) == 1:
                # means we're getting
                pass

        return _on_change

    def __call__(self, *args, **kwargs):
        ret = []
        for domain_name in self._domains:
            domain = self._domains[domain_name]
            ret.append(domain(*args, **kwargs))
        return ret

    def __getattr__(self, attr: str) -> SingleDomainComparator:
        if attr in self._domains:
            return self._domains[attr]

    @property
    def domain(self):
        return self._operation_domain

    @domain.setter
    def domain(self, arr: list):
        # call the super class's setter
        super(MultiDomainComparator, self.__class__).domain.fset(self, arr)
        for domain_name in self._domains:
            self._domains[domain_name].domain = arr


class TimeFreqDomainComparator(MultiDomainComparator):

    def __init__(self):
        domains = {
            "time": TimeDomainComparator("time"),
            "freq": FrequencyDomainComparator("freq")
        }

        super(TimeFreqDomainComparator, self).__init__(domains=domains)
