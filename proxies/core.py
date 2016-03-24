"""
    proxies3.proxies.core
    ~~~~~~~~~~~~~~~~~~~~

"""
from collections import ChainMap

class BaseDict(dict):
    """ dict wrapper that returns self on update instead of none-type.  This allows us to
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

class BaseViewContext(BaseDict):
    """ A dict object that on update returns self to allow method chaining to be easier.
        Also will raise an error if a render method is not implemented.
    """
    def render(self, *args, **kwargs):
        raise NotImplementedError('render method not implemented for \'{}\''\
                .format(self.__class__.__name__))

