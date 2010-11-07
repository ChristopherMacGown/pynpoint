""" A class that handles mixins """


class Mixin(object):
    """ Class that handles callable mixins """
    registered_mixins = {}

    def __init__(self, target, mixin):
        self.target = target
        self.mixin = mixin

    def __enter__(self):
        """ Allows us to use with syntax to dynamically load a mixin into a
            target class """
        return self.__load()

    def __exit__(self, *args):
        """ Allows us to use with syntax to dynamically unload a mixin from a
            target class """
        self.__unload()

    def __load(self):
        """ load the mixin into the target's class.__bases__ """
        self.target.__class__.__bases__ += (self.mixin,)
        return self.target

    def __unload(self):
        """ unload the mixin from target's class.__bases__ """
        bases = list(self.target.__class__.__bases__)
        bases.remove(self.mixin)
        self.target.__class__.__bases__ = tuple(bases)

    @classmethod
    def get_mixin(cls, key):
        """ Given a key, return a mixin """
        return cls.registered_mixins.get(key, None)

    @classmethod
    def register(cls, key, mixin):
        """ Register a mixin with a key """
        if not cls.registered_mixins.get(key, None):
            cls.registered_mixins[key] = mixin

        return cls.registered_mixins[key]

    @classmethod
    def unregister(cls, key):
        """ Unregister the mixin so it can no longer be used """
        if key in cls.registered_mixins:
            return cls.registered_mixins.pop(key)
