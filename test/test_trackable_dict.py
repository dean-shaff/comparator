import unittest

from comparator.trackable_dict import TrackableDict


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


if __name__ == "__main__":
    unittest.main()
