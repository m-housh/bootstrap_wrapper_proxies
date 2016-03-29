"""
    proxies.context_registry
    ~~~~~~~~~~~~~~~~~~~~~~~~
"""
from inspect import isclass
from collections import namedtuple
from .core import BaseViewContext
from .utils import TypeParser, get_first

ContextContainer = namedtuple('Context', ['key', 'context'])

class InvalidContextError(TypeError):

    def __init__(self, text=None):
        if text is None:
            text = 'context must inherit from BaseViewContext'
        super().__init__(text)
   
get_first_string = get_first(TypeParser(str))

class ContextRegistry:

    def __init__(self, *args, **kwargs):
        self.contexts = []
        
        key, context = self._parse_args(args, kwargs)
        if context is not None:
            context, error = self._validate_context(context)
            if error:
                raise error
            
            if key is None:
                key = 'default'

            self.contexts.append(ContextContainer(key, context))

    
    def _validate_context(self, context):
        error = None
        if isclass(context):
            if not context is BaseViewContext and \
                    BaseViewContext not in context.__bases__:
                error = InvalidContextError()
        elif not isinstance(context, BaseViewContext):
            error = InvalidContextError()
        return (context, error)

    def _parse_args(self, args, kwargs):
        """ allows us to init class with args or kwargs. """
        key = None
        context = None
        # try from args first
        # get the first string to use as a key
        key = get_first_string(args)
        if key is not None:
            # if we found a key then reset args to everything that is not key
            args = tuple(arg for arg in args if arg is not key)
        # check args/remaining args for a context 
        if len(args) == 1:
            context = args[0]
        # should possibly do something here if there's too many args
        
        # next try to get from kwargs if not found
        if key is None:
            key = kwargs.get('key')
        if context is None:
            context = kwargs.get('context')

        return (key, context)
        
    def get(self, key, default=None):
        try:
            return next(item[1] for item in self.contexts if item[0] == key)
        except StopIteration:
            return default

    def keys(self, r_type='tuple'):
        """ if r_type is None return a generator else return r_type. """
        r_type = { 'list': list, 'tuple': tuple }.get(r_type, r_type) 
        rv = (item[0] for item in self.contexts)
        if r_type is None:
            return rv
        return r_type(rv)

    def values(self, r_type='tuple'):
        r_type = { 'list': list, 'tuple': tuple }.get(r_type, r_type)
        rv = (item[1] for item in self.contexts)
        if r_type is None:
            return rv
        return r_type(rv)

    def __setitem__(self, key, context):
        context, error = self._validate_context(context)
        if error:
            raise error
        
        # should check if key exists first
        if key in self.keys():
            # deletw item by index if exists, bc we can't update a namedtuple, we must
            # make a new one
            del(self.contexts[self.contexts.index((key, self.get(key)))])

        self.contexts.append(ContextContainer(key, context))


    def __getitem__(self, key):
        rv = self.get(key)
        if rv is not None:
            return rv
        raise KeyError(key)

    def __getattr__(self, key):
        rv = self.get(key)
        if rv is not None:
            return rv
        raise AttributeError(key)


