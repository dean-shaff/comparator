## Comparator

[![Build Status](https://travis-ci.org/dean-shaff/comparator.svg?branch=master)](https://travis-ci.org/dean-shaff/comparator)

### Install

```
python setup.py install
```

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
# Alternatively, do the following:
comp.freq.set_fft_size(2**15)
comp.operators["diff"] = lambda a, b: np.abs(a - b)
comp.products["mean"] = np.mean
comp.time.operators["xcorr"] = lambda a, b: scipy.signal.fftconvolve(a, b.conj)
comp.time.products["max"] = np.amax

# generate some random data to compare
a, b, c = [np.random.rand(100) + 1j*np.random.rand(100) for i in range(3)]

res = comp(a,b,c)
# or if you want something specific:
comp.freq.polar(a, b, c)
comp.freq(a, b, c)
comp.time(a, b)

comparator.util.corner_plot(res)
plt.show()
```
