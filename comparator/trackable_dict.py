
__all__ = [
    "TrackableDict"
]


class TrackableDict(dict):

    def __init__(self, *args, **kwargs):

        super(TrackableDict, self).__init__(*args, **kwargs)
        self._listeners = []

    def __getitem__(self, item):

        for callback in self._listeners:
            try:
                callback(item)
            except TypeError:
                pass

        return super(TrackableDict, self).__getitem__(item)

    def __setitem__(self, item, val):
        for callback in self._listeners:
            try:
                callback(item, val)
            except TypeError:
                pass

        return super(TrackableDict, self).__setitem__(item, val)

    def on(self, callback):
        self._listeners.append(callback)
        # if item not in self._listeners:
        #     self._listeners = [callback]
        # else:
        #     self._listeners.append(callback)
