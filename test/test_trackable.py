import unittest

from comparator.trackable import (
    TrackableDict,
    TrackableList
)


class Callback:
    """
    Testing callback. Do not use for any production code, as this is
    (deliberately) not memory efficient!
    """
    def __init__(self):
        self.called = False
        self.called_count = 0
        self.args = []

    def __call__(self, *args):
        self.called = True
        self.called_count += 1
        self.args.append(args)


class TestTrackableDict(unittest.TestCase):

    def test_on(self):
        callback = Callback()
        d = TrackableDict({"person": 23})
        d.on(callback)
        d["person"] = 25
        d["person"]
        self.assertTrue(callback.called)
        self.assertTrue(callback.called_count == 2)
        self.assertTrue(callback.args[0] == ("person", 25))
        self.assertTrue(callback.args[1] == ("person", ))


class TestTrackableList(unittest.TestCase):

    def test_on(self):
        callback = Callback()
        d = TrackableList([0, 10, 10])
        d.on(callback)
        d[0] = 25
        d[1]
        self.assertTrue(callback.called)
        self.assertTrue(callback.called_count == 2)
        self.assertTrue(callback.args[0] == (0, 25))
        self.assertTrue(callback.args[1] == (1, ))


if __name__ == "__main__":
    unittest.main()
