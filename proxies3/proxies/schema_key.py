"""
    proxies3.proxies.schema_key
"""
from collections import ChainMap

class SchemaKey(dict):
   
    def update(self, kwargs):
        super().update(kwargs)
        return self

class SchemaMap(ChainMap):

    def update(self, kwargs):
        super().update(kwargs)
        return self


class SchemaLabelMeta(type):
    def __init__(cls, name, bases, attrs):
        if name != 'SchemaLabelProtocol':
            error = True
            if hasattr(cls, '_labels'):
                labels = cls._labels
                if isinstance(labels, SchemaMap):
                    error = False
                if isinstance(labels, SchemaKey):
                    cls._labels = SchemaMap(labels)
                    error = False
                elif isinstance(labels, dict):
                    cls._labels = SchemaMap(SchemaKey(labels))
                    error = False

            if error is True:
                raise NotImplementedError('_labels attr is not implemented for \'{}\''\
                        .format(name))

        return type.__init__(cls, name, bases, attrs)


    @property
    def labels(self):
        return self._labels

class SchemaLabelProtocol(metaclass=SchemaLabelMeta):

    @property
    def labels(self):
        return type(self).labels
