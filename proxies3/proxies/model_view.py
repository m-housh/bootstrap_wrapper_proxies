"""
    proxies3.proxies.model_view
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from .core import BaseChainMap
from .schema_key import SchemaLabelProtocol, SchemaLabelMeta

class ViewContextMap(BaseChainMap):
    pass

class ModelView:

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


class FormViewProxy:
    _form_ctx = ViewContextMap()

    def __init__(self, modelView, form):
        self.model_view = modelView
        self.form = form
