## Comparator

[![Build Status](https://travis-ci.org/dean-shaff/comparator.svg?branch=master)](https://travis-ci.org/dean-shaff/comparator)

### Usage


```python
c = MultiDomainComparator()
c.add_domain("time") # base domain
c.add_domain("freq", np.fft.fft, np.fft.ifft)
c.time.domain("all")
c.freq.domain([0, 2**15])
c.operators["diff"] = lambda a, b: np.abs(a - b)
c.products["mean"] = np.mean
c.time.operators.xcorr = lambda a, b: scipy.signal.fftconvolve(a, b.conj)
c.time.products["max"] = np.amax
c.freq.polar(a, b, c).json()
c.freq(a, b, c).json()
c.time(a, b).json()
```
