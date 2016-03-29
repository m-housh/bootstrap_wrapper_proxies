from collections import ChainMap
from .utils import OrderedLabels

class BaseDict(dict):
    
    def __getattr__(self, key):
        """ allow dot style access to key values """
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        return self

class BaseChainMap(ChainMap):

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        return self


class BaseViewContext:
    label_order = {}

    def __init__(self, *, model=None, labels=None, label_order=None):
        if label_order is not None:
            self.label_order = label_order

        if model is None:
            raise ValueError('must supply a model_class.')
        else:
            self.model = model
        
        if labels is None:
            labels = {}

        self.labels = OrderedLabels(labels, self.label_order)

    def render(self):
        raise NotImplementedError('render method not implemented for {}'\
                .format(self.__class__.__name__))


class BaseErrorHandler:

    def handle_error(self, error):
        raise error
