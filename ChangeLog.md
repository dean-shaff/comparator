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
