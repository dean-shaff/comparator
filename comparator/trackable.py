
__all__ = [
    "TrackableDict",
    "TrackableList"
]


def trackable(super_cls):
    def _trackable(cls):
        class Trackable(super_cls):

            def __init__(self, *args, **kwargs):

                super(Trackable, self).__init__(*args, **kwargs)
                self._listeners = []

            def __getitem__(self, item):

                for callback in self._listeners:
                    try:
                        callback(item)
                    except TypeError:
                        pass

                return super(Trackable, self).__getitem__(item)

            def __setitem__(self, item, val):
                for callback in self._listeners:
                    try:
                        callback(item, val)
                    except TypeError:
                        pass

                return super(Trackable, self).__setitem__(item, val)

            def on(self, callback):
                self._listeners.append(callback)
        return Trackable
    return _trackable


@trackable(dict)
class TrackableDict:
    pass


@trackable(list)
class TrackableList:
    pass
