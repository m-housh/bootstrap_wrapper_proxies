"""
    proxies3.proxies.model_view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from .core import BaseChainMap, BaseDict
from .schema_key import SchemaLabelProtocol, SchemaLabelMeta

class ViewContextMap(BaseChainMap):
    """ A ChainMap class that maps view contexts on our ModelViewProxy class. Implements
        update which returns self instead of None to make chaining methods easier, if 
        necessary.
    """
    pass

class ViewContext(BaseDict):
    """ A dict object that on update returns self to allow method chaining to be easier.
        Also will raise an error if a render method is not implemented.
    """
    def render(self, *args, **kwargs):
        raise NotImplementedError('render method not implemented for \'{}\''\
                .format(self.__class__.__name__))


class ModelViewProxy:
    """ A proxy object for a db Model class that allows for view contexts to be added. 

        The class needs to implement SchemaLabelProtocol to supply human readable labels
        to be rendered in the different view contexts.

        Meant to wrap a class and register different named contexts to be able to
        easily render different views depending on the context (ex. form, table, etc...).
        
        The render method's should be able to handle an instance or list of instances of 
        the class the ModelViewProxy is associated with and render them in the given
        context.
    """
    #:TODO: offer a method that allows a full context to be passed in at render for instances
    #       where it doesn't make sense to register a different context on our ModelViewProxy.
    #       render_with_context(context)
    def __init__(self, modelClass, **kwargs):
        if not isinstance(modelClass, (SchemaLabelMeta, SchemaLabelProtocol)):
            err_msg = 'model \'{}\' does not implement SchemaLabelProtocol.'\
                    .format(modelClass.__name__)
            raise TypeError(err_msg)
        if isinstance(modelClass, SchemaLabelMeta):
            # if modelClass was passed in as a class it will be an instance of SchemaLabelMeta
            # set our _modelClass attribute to the passed in class
            self._model_class = modelClass
        if isinstance(modelClass, SchemaLabelProtocol):
            # if modelClass was passed in as in instance we set our our _modelClass attribute
            # to the instances class
            self._model_class = modelClass.__class__
        # set labels with a new context, so any changes don't get reflected on the
        # parent class
        self.labels = self._model_class.labels.new_child()
        self._view_ctx = ViewContextMap({'labels': self.labels})


    def register_context(self, key, context):
        if not isinstance(context, ViewContext) and isinstance(context, dict):
            context = ViewContext(context)
        elif not hasattr(context, 'render'):
            raise TypeError('context must implement a render method')

        # should probably check if key exists in the _view_ctx and add a new_child
        # if it does
        self._view_ctx.update({ key: context })


    def _get_ctx(self, context):
        """ get a context from our _view_ctx mapping. """
        ctx = None
        error = None
        try:
            ctx = self._view_ctx[context]
        except KeyError as e:
            error = e

        return (ctx, error)

    def _get_render_for_context(self, context):
        """ get a render method for a context. """
        ctx, error = self._get_ctx(context)
        render = None
        if ctx is not None:
            try:
                render = ctx['render']
            except KeyError as e:
                error = e

        return (render, error)

    def render(self, context, *args, **kwargs):
        """ call render on a given context name. """
        render, error = self._get_render_for_context(context)

        if render is None:
            raise KeyError('{} does not have \'{}\' context or context does not implement \
                    a render method'\
                    .format(self.__class__.__name__, context))

        return render(*args, **kwargs)

