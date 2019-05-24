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

### v0.7.2

- Can now set the operation domain directly with a `slice` object.
- Added unit test to check for setting the operation domain.

### v0.7.3

- Fixed bug in `NumpyEncoder` where we couldn't encode `numpy.float32`
objects. We can now, in principle, encode any of numpy's basic int and float
types.
- Added tests in `test.test_util` to test for numpy int and float
compatibability.

### v0.8.0

- Added an `ComparatorOperatorResult` object. This is a representation of the operator
result. Supports Numpy-like indexing.
- Added the ability to label `ComparatorOperatorResult` and `ComparatorProductResult`
objects. This makes it a little easier to keep track of the progress of specific
vectors as they progress through the `comparator` processing chain.
- `SingleDomainComparator.__call__` now takes a `labels` keyword argument.
- Changing the `domain` attribute of a `MultiDomainComparator` changes the
operation domain for each of the constituent comparator objects.

### v0.8.1

- `util.plot_operator_result` now plots with labels.

### v0.8.2

- `util.plot_operator_result` takes `**kwargs`, which get passed to `plt.subplots`
- `util.plot_operator_result` puts axis ylabels on right side.

### v0.8.3

- `FrequencyDomainComparator` doesn't attempt to time align data before
transforming.

### v0.8.4

- Attempting to fix bug in `TimeDomainComparator.get_time_delay` where finding
the maximum of a complex array is at best ambiguous.


### v0.9.0

- When using complex data, instead of operating on complex components independently,
we operate them as a whole, only separating at the end.

### v0.9.1

- util.plot_operator_result returns tuple of dictionaries instead of tuple of
lists.
- util.plot_operator_result puts correct complex representation as ylabels, eg
if we're using cartesian, then "Real" and "Imaginary" are the ylabels.

### v0.10.0

- I got tired of trying to split things into different representations of complex
numbers. Its impossible to keep track of. If a number is complex, leave it complex.
- I changed the way ComparatorProductResult objects are indexed. I got tired of
writing things like `list(res_prod[0, 1])['mean']`. Instead we can just do
`res_prod["mean"][0][1]` or even `res_prod[0, 1]["mean"]`.
- We can produce a corner plot with `plot_operator_result`. This only
make sense for symetric operators, trivially non symetric operators (like the
difference). For some operators, like cross correlation, corner plots may not
be necessary.
- `plot_operator_result` takes an optional complex representation, which
handles complex data, if applicable.
- `plot_operator_result` can work with single operator result objects. We can
do something like the following:

```python
>>> res_op, res_prod = comp(*data)
>>> util.plot_operator_result(res_op["diff"])
```

- The `SingleDomainComparator` supports specfying the domain as a fraction of
the total domain:
```python
comp = comparator.SingleDomainComparator("domain_name")

comp.domain = [0, 0.1]
```
Here, `comparator` would automatically know to only analyze the first 10th of
the data. This is useful when we don't know or don't care about the length of
the input a priori.
