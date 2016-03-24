"""
    proxies.contexts
    ~~~~~~~~~~~~~~~~
"""
from .core import BaseViewContext
from .utils import OrderedLabels

from bootstrap_wrapper import Table, Div, TableHeader, TableRow
from inspect import isclass

class ViewContext(BaseViewContext):
    """ A view context wrapper around an bootstrap_wrapper html_tag. """
    tag = Div
    label_order = None

    def __init__(self, *args, model=None, labels=None, label_order=None, **kwargs):
        self.model = model
        self.label_order = label_order or {}

        self.labels = OrderedLabels(labels, self.label_order)

        if isclass(self.tag):
            self.tag = self.tag()


    def add(self, *args, **kwargs):
        return self.tag.add(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self.tag.render(*args, **kwargs)


class TableViewContext(ViewContext):
    tag = Table
    
    def header(self, **kwargs):
        return self.tag.add(TableHeader(
            *self.labels.values(),
            **kwargs))

    
    def row(self, model_instance, *args, **kwargs):
        return self.tag.add(TableRow(
            *[getattr(model_instance, key) for key in self.labels.keys()], 
            **kwargs))

    def render(self, model_instances, header=True, **kwargs):
        if header:
            self.header()

        if isinstance(model_instances, (tuple, list)):
            for model in model_instances:
                self.row(model)
        else:
            self.row(model_instances)
        
        return self.tag.render(**kwargs)



