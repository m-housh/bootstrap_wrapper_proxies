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
    """ SchemaLabelMeta enforces all classes that implement SchemaLabelProtocol have
        a _label attribute.  The _label attribute can be a dict, SchemaKey, or SchemaMap
        object, however will always get transformed into a SchemaMap during creation of
        a class. The SchemaMap class allows us to have inherit labels, but use them in 
        a different context, so that updates don't always get reflected on other sub-classes
        unless the label is changed on the base-class that declares that label property.
    """
    def __init__(cls, name, bases, attrs):
        labels = SchemaMap()
        # get bases of the class
        bases = [base for base in bases if base.__name__ != 'SchemaLabelProtocol']
        maps = []
        # get the label maps from the bases if applicable
        for base in bases:
            if hasattr(base, '_labels'):
                # get all the maps from base classes
                maps += [_map for _map in base._labels.maps \
                        if _map not in maps and _map not in labels.maps]
        # update our SchemaMap instance with base class values
        if len(maps) > 0:
            for _map in maps:
                # update labels
                labels.update(_map)
            # insert a new context in the front of our labels
            labels.maps.insert(0, {})
        # allow base class to not throw errors if it does not have a _labels
        # attribute, however enforce on sub-classes of base class ('SchemaLabelProtocol')
        if name != 'SchemaLabelProtocol':
            error = True
            if hasattr(cls, '_labels'):
                if isinstance(cls._labels, SchemaMap):
                    error = False
                    labels.update(cls._labels)
                if isinstance(cls._labels, SchemaKey):
                    labels.maps.append(cls._labels)
                    error = False
                elif isinstance(cls._labels, dict):
                    labels.maps.append(SchemaKey(cls._labels))
                    error = False
                # set labels on the new class
                cls._labels = labels
            # error if not implemented for a sub-class
            if error is True:
                raise NotImplementedError('_labels attr is not implemented for \'{}\''\
                        .format(name))

        return type.__init__(cls, name, bases, attrs)

    @property
    def labels(self):
        """ Make _labels accessible in a more friendly way, this is on the meta-class,
            so it's not accessible from instances without calling type(instance)
        """
        return self._labels

class SchemaLabelProtocol(metaclass=SchemaLabelMeta):
    """ Enforces the _label attribute on sub-classes. """
    pass
