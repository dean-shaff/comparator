### v0.6.0

- Fixed bug in `ComparatorProductResult` where it couldn't call `__iter__`
on a product resulting from a vector -> vector operation.
- Cleaned up tests for `ComparatorProductResult` such that it reads data
in from a JSON file instead of having the data stored in the `setUpClass`
class method.
- Added __str__ method to `ComparatorProductResult` that prints out the
contents of the object.
- Added __format__ method to `ComparatorProductResult` that allows us to
format `ComparatorProductResult` objects as we please!
- Fixed bug in `NumpyEncoder` where we couldn't dump `numpy.int64` objects.

### v0.6.1

- Fixed bug in `setup.py` where matplotlib dependency wasn't declared.
- `util.corner_plot` not working.

### v0.7.0

- Renamed `util.corner_plot` to `util.plot_operator_result`
- Added the ability for `util.plot_operator_result` to plot data from an operator that
takes a single argument. In this case, it doesn't actually create a corner plot,
rather it's just a single column.
- Added tests for new `util.plot_operator_result` functionality.
- Got rid of unnecessary `copy` import in `single_domain.py`
- Thinking about adding an `OperatorResult` object that contains some meta data
about the operator result (is it cartesian or polar complex representation, for example).
- Right now, when we supply complex data, the `SingleDomainComparator` object
breaks the data into cartesian or polar representations. I'd like to be able
to do operations on complex data as a whole. This would require a bit of work
to overhaul.

### v0.7.1

- Fixed `test_comparator_import.py` to reflect new API, introduced in v0.7.0
