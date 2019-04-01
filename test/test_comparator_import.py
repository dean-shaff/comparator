import unittest


class TestComparatorImport(unittest.TestCase):

    def test_comparator_import(self):
        from comparator import (
            SingleDomainComparator,
            TimeDomainComparator,
            FrequencyDomainComparator,
            MultiDomainComparator,
            TimeFreqDomainComparator,
            plot_operator_result,
            NumpyEncoder
        )


if __name__ == "__main__":
    unittest.main()
