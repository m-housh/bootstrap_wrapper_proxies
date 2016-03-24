"""
    proxies3.proxies.core
    ~~~~~~~~~~~~~~~~~~~~

"""
from collections import ChainMap

class BaseDict(dict):
    """ dict wrapper that returns self on update instead of non-type.  This allows us to
        chain methods together.
    """
    def update(self, kwargs):
        super().update(kwargs)
        return self

class BaseChainMap(ChainMap):
    """ ChainMap wrapper that returns self on update instead of none-type.  This allows us
        to chain methods together.
    """
    def update(self, kwargs):
        super().update(kwargs)
        return self

