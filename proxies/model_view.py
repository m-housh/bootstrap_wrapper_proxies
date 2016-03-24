"""
    proxies.model_view
    ~~~~~~~~~~~~~~~~~~
"""
from inspect import isclass


from .core import BaseChainMap, BaseViewContext
from .schema_helpers import SchemaLabelProtocol, SchemaLabelMeta


class ViewContextMap(BaseChainMap):
    """ A ChainMap class that maps view contexts on our ModelViewProxy class. Implements
        update which returns self instead of None to make chaining methods easier, if 
        necessary.
    """
    pass


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
            self.model_class = modelClass
        if isinstance(modelClass, SchemaLabelProtocol):
            # if modelClass was passed in as in instance we set our our _modelClass attribute
            # to the instances class
            self.model_class = modelClass.__class__
        # set labels with a new context, so any changes don't get reflected on the
        # parent class
        self.labels = self.model_class.labels.new_child()
        self._view_ctx = ViewContextMap({'labels': self.labels})


    def register_context(self, key, context, *args, **kwargs):
        """ Register a context object with this model view. The context should most likely
            be a class, or a dict like object.  If the context is a class this method
            will initialize that class passing in a reference to the model_class for this 
            model_view and will get a labels context passed in.  So the class must
            accept kwargs for these items it is easiest for these contexts to be a sub-class
            of ViewContext which accept these arguments by default. Any *args, **kwargs get
            passed along to the class for instantiation.
        """ 
        _context = None
        if isclass(context):
            _context = context(*args, 
                    model=self.model_class, 
                    labels=self.labels.new_child(),
                    **kwargs)
        # not sure I need to do this, possibly just check for a render attribute and
        # that the render attribute is callable
        '''
        if not isinstance(context, BaseViewContext):
            # coerce context into a BaseViewContext class.
            context = BaseViewContext(context)
        ''' 
        '''
        if not hasattr(context, 'render'):
            raise TypeError('context must implement a render method')
        '''
        if _context is not None:
            self._view_ctx.update({ key: _context })
        else:
            # error
            pass


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
                render = ctx.render
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

