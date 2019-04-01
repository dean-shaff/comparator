## Comparator

[![Build Status](https://travis-ci.org/dean-shaff/comparator.svg?branch=master)](https://travis-ci.org/dean-shaff/comparator)

### Install

```
python setup.py install
```

If you're using poetry, you can add `comparator` to your git sources:

```toml
# pyproject.toml
[tool.poetry.dependencies]
comparator = {git = "git@github.com:dean-shaff/comparator.git"}
```

Now calling `poetry update` will install `comparator`

### Usage

`comparator` offers a simple interface for comparing single dimensional
arrays, either real or complex. Each `comparator` object has associated
with it "operators", "products", and a "domain". "Operators" are operations
that apply to pairs of arrays, producing a single array as output. Examples
might be cross correlation and difference squared. "Products"
are operation that apply to single arrays, producing a single number as output.
Examples include mean and max. The "domain" is the subset of input arrays on
which to operate.

```python
import matplotlib.pyplot as plt
import comparator.util
from comparator import TimeFreqDomainComparator

comp = TimeFreqDomainComparator()
comp.freq.domain = [0, 2**15]
# we can also set the domain with a slice object:
comp.freq.domain = slice(0, None)
# Alternatively, do the following:
comp.freq.set_fft_size(2**15)

# operators can map from any number of inputs to a single output.
# Its convenient to operate on the input arrays themselves, hence 'this'
comp.operators["this"] = lambda a: a
comp.operators["diff"] = lambda a, b: np.abs(a - b)
comp.products["mean"] = np.mean
# only the time domain will have the cross correlation ("xcorr") operator
comp.time.operators["xcorr"] = lambda a, b: scipy.signal.fftconvolve(a, b.conj)
# only the time domain will have the "max" product
comp.time.products["max"] = np.amax

# generate some random data to compare
a, b, c = [np.random.rand(100) + 1j*np.random.rand(100) for i in range(3)]

res_prod, res_op = comp(a, b, c)
# print out the result product matrix or array in scientific notation
print(f"{res_prod:.4e}")
# util has a corner plot utility
comparator.util.corner_plot(res_op)
plt.show()

# Instead of calling the Comparator object itself, we could get something
# specific from each of the subdomains:
comp.freq.polar(a, b, c)
comp.freq(a, b, c)
comp.time(a, b)
```
