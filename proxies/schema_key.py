"""
    proxies.schema_key
    ~~~~~~~~~~~~~~~~~
"""
from .core import BaseDict, BaseChainMap

class SchemaKey(BaseDict):
    """ A dict object that the keys should map to model attributes and values should be
        a human friendly label to be used in a view context (form, table, etc.)

        On updates it returns self instead of None to be able to chain methods together.
    """    
    pass
   
class SchemaMap(BaseChainMap):
    """ A ChainMap object that chains dict's together.  This allows us to declare a SchemaKey
        on a model mixin and chain those values to models that use the mixin.  This gives
        each model a new context, so that changing values on a model does not change them
        for every other model that uses that key, unless specifically changed on the base
        model/mixin during class creation.  If key get's changed after class creation then
        it only get's updated in that context. (see tests for more details).
    """
    pass

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
            if hasattr(base, 'labels'):
                # get all the maps from base classes
                maps += [_map for _map in base.labels.maps \
                        if _map not in maps and _map not in labels.maps]
        # update our SchemaMap instance with base class values
        if len(maps) > 0:
            for _map in maps:
                # update labels
                labels.update(_map)
            # insert a new context in the front of our labels
            labels.maps.insert(0, {})
        # allow base class to not throw errors if it does not have a labels
        # attribute, however enforce on sub-classes of base class ('SchemaLabelProtocol')
        if name != 'SchemaLabelProtocol':
            error = True
            if hasattr(cls, 'labels'):
                if isinstance(cls.labels, SchemaMap):
                    error = False
                    labels.update(cls.labels)
                if isinstance(cls.labels, SchemaKey):
                    labels.maps.append(cls.labels)
                    error = False
                elif isinstance(cls.labels, dict):
                    labels.maps.append(SchemaKey(cls.labels))
                    error = False
                # set labels on the new class
                cls.labels = labels
            # error if not implemented for a sub-class
            if error is True:
                raise NotImplementedError('_labels attr is not implemented for \'{}\''\
                        .format(name))

        return type.__init__(cls, name, bases, attrs)
    
class SchemaLabelProtocol(metaclass=SchemaLabelMeta):
    """ Enforces the label attribute on sub-classes. """
    pass
