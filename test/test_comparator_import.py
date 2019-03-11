import unittest


class TestComparatorImport(unittest.TestCase):

    def test_comparator_import(self):
        from comparator import (
            SingleDomainComparator,
            TimeDomainComparator,
            FrequencyDomainComparator,
            MultiDomainComparator,
            TimeFreqDomainComparator,
            corner_plot,
            NumpyEncoder
        )


if __name__ == "__main__":
    unittest.main()
