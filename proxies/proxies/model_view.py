"""
    proxies.model_view
    ~~~~~~~~~~~~~~~~~~
"""
from inspect import isclass
from .core import BaseViewContext, BaseDict, BaseErrorHandler
from .schema_helper import SchemaLabelMeta, SchemaLabelProtocol
from .utils import TypeParser
from .context_registry import ContextRegistry, InvalidContextError

get_strings = TypeParser(str)

class BaseModelViewProxy:
    """ This is the main object that we interact with.  We can register views and group
        by keys and a sub-key for the view, which allows us to have similar view groups
        and choose them based on key.sub-key string passed in to the render function.
        Each view context get's a reference to the db.Model class that it is associated with
        and a reference to the SchemaLabel's.  All registered view contexts should inherit
        from BaseViewContext to ensure that they can handle the render method as well
        as instantiation with the correct kwargs ({'model': ..., 'labels':...}).  A registered
        view context can be a class(preferrable) or an instance.  If it is class then we
        will instantiate that class in the render function passing in the db.Model and Labels,
        then call render on it passing along any args or kwargs to the render function of
        the view context.  This class also offers a convenience method to make a new context
        instance from an existing key.sub-key pair, that could then be re-registered with a
        different sub-key.  This is so if you have a view that's very similar, but needs a
        little bit different set-up then it can be done easily. The render method does not
        have to render a view that is registered with this instance, it can also accept
        an instance of view context and render it with the passed in args and kwargs.
    """

    def __init__(self, model_class, *args, **kwargs):
        if not isinstance(model_class, (SchemaLabelMeta, SchemaLabelProtocol)):
            if isclass(model_class):
                name = model_class.__name__
            else:
                name = model_class.__class__.__name__
            raise TypeError("model '{}' does not implement SchemaLabelProtocol"\
                    .format(name))

        if isinstance(model_class, SchemaLabelMeta):
            self.model_class = model_class
        elif isinstance(model_class, SchemaLabelProtocol):
            self.model_class = model_class.__class__

        self.labels = self.model_class.labels
        self.registerys = BaseDict()
        
    def register_context(self, key, sub_key, context):
        """ Register a sub-context with an existing registry or create a new registry if
            one does not exist on this instance for the given key. 
            
            :param key:         The key for an existing registry or key for a new registry.
            :param sub_key:     The sub-key for the context being registered. 
            :param context:     The context to be registered.  Will raise InvalidContextError
                                if the context does not inherit from BaseViewContext.
            :returns:           None
        """
        # :TODO: these could raise an InvalidContextError if context is invalid type,
        #        so should register with an error handler when I get that done
        if key in self.registerys:
            self.registerys[key][sub_key] = context
        else:
            self.registerys[key] = ContextRegistry(sub_key, context)
        
    
    def _get_context_keys(self, args):
        """ helper to parse args into key, sub-key, error tuple. """
        key = None
        sub_key = None
        error = None
        if isinstance(args, str):
            strings = [args]
        else:
            strings = get_strings(args, list)
        if len(strings) > 0:
            if len(strings) == 1:
                if '.' in strings[0]:
                    split = strings[0].split('.')
                    key, sub_key = split
                else:
                    key = strings[0]
            elif len(strings) == 2:
                key, sub_key = strings
            elif len(strings) > 2:
                error = ValueError('too many strings to parse context')
        else:
            error = ValueError('must pass in a string to get a context')

        return (key, sub_key, error)


    def get_context(self, *args):
        """ Get a context from this instance.  Can either return a sub-context or the entire
            registery for a key.

            :param args:        Should contain only strings.  Can be (key, sub-key) which
                                would return a sub-context, (key.sub-key) which would
                                return a sub-context, or (key) which would return the
                                registry for that key.

            :returns:           Either sub-context or a registry.
        """
        key, sub_key, error = self._get_context_keys(args)
        if error:
            raise error

        if key not in self.registerys:
            raise KeyError(key)

        rv = self.registerys[key]
        if sub_key is not None:
            rv = rv.get(sub_key)
            if rv is None:
                raise KeyError(sub_key)
            return rv
        return rv
    
    def init_context(self, key, sub_context, *args, **kwargs):
        """ A convenience method to instantiate a new context based on a key, sub-key. 
        
            :returns:   A new instance of the context asked for 
        """
        context_class = self.get_context(key, sub_context)
        if not isclass(context_class):
            context_class = context_class.__class__

        kwargs.update({'model': self.model_class, 'labels': self.labels})
        context = context_class(*args, **kwargs)
        return context

    def render(self, context, *args, **kwargs):
        """ Render's a context.
            
            :param context:     Can be a string with dot-style syntax for key.sub-key context
                                access, an instance of a context, or a class of a context
                                that we will instantiate with a Model reference and Label
                                reference then call render on it with that passed in args and
                                kwargs.

            :param args:        args to be passed on to the context's render method
            :param kwargs:      kwargs to be passed on to the context's render method

            :returns:           A markupsafe string to be used as a view or context for
                                an html body.
        """
        if isinstance(context, str):
            key, sub_key, error = self._get_context_keys(context)
            if error:
                raise error

            if key is not None and key in self.registerys:
                if sub_key is not None:
                    try:
                        context = self.get_context(key, sub_key)
                    except KeyError as e:
                        # should make a sub-key error object
                        raise e
                else:
                    try:
                        context = self.get_context(key, 'default')
                    except KeyError:
                        raise ValueError('invalid sub-key and no default registered')
            elif key is not None:
                raise KeyError(key)

        if isclass(context):
            context = context(**{'model': self.model_class, 'labels': self.labels})
        return context.render(*args, **kwargs)


class ModelViewProxy(BaseModelViewProxy):
    """ Wraps all of BaseModelViewProxy's methods in an error handler.  That can be registered
        with this instance.
    """
    def __init__(self, model_class, error_handler=None, *args, **kwargs):
        if error_handler is not None:
            self.error_handler = error_handler
        else:
            self.error_handler = BaseErrorHandler()
        try:
            super().__init__(model_class, *args, **kwargs)
        except TypeError as e:
            self.error_handler.handle_error(e)

    def register_context(self, *args, **kwargs):
        try:
            return super().register_context(*args, **kwargs)
        except InvalidContextError as e:
            return self.error_handler.handle_error(e)

    def get_context(self, *args, **kwargs):
        try:
            return super().get_context(*args, **kwargs)
        except KeyError as e:
            return self.error_handler.handle_error(e)
    
    def init_context(self, *args, **kwargs):
        try:
            return super().init_context(*args, **kwargs)
        except Exception as e:
            return self.error_handler.handle_error(e)

    def render(self, *args, **kwargs):
        try:
            return super().render(*args, **kwargs)
        except Exception as e:
            return self.error_handler.handle_error(e)
