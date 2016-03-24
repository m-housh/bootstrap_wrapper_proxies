"""
    proxies.contexts
    ~~~~~~~~~~~~~~~~
"""
from .core import BaseViewContext
from .utils import OrderedLabels

from bootstrap_wrapper import Table, Div, TableHeader, TableRow, ResponsiveTable
from inspect import isclass

class ViewContext(BaseViewContext):
    """ A view context wrapper around an bootstrap_wrapper html_tag. """
    tag = Div
    label_order = None

    def __init__(self, *args, model=None, labels=None, label_order=None, **kwargs):
        self.model = model
        self.label_order = label_order or {}

        self.labels = OrderedLabels(labels, self.label_order)

        if not isclass(self.tag):
            self.tag = self.tag.__class__

    def render(self, *args, tag_kwargs=None, **kwargs):
        if not tag_kwargs:
            tag_kwargs = {}

        tag = self.tag(**tag_kwargs)

        return tag.render(*args, **kwargs)


class TableViewContext(ViewContext):
    tag = ResponsiveTable
   
    def __init__(self, *args, responsive=True, bordered=False, striped=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not responsive:
            self.tag = Table

        self.bordered = bordered
        self.striped = striped


    def header(self, **kwargs):
        return TableHeader(
            *self.labels.values(),
            **kwargs)

    
    def row(self, model_instance, *args, **kwargs):
        return TableRow(
            *[getattr(model_instance, key) for key in self.labels.keys()], 
            **kwargs)

    def render(self, model_instances, header=True, tag_kwargs=None, **kwargs):
        tag = None
        if tag_kwargs is not None:
            if not isinstance(tag_kwargs, dict):
                # error
                pass
        else:
            tag_kwargs = {}

        if self.tag is ResponsiveTable:
            tag = self.tag()
        
        bordered = tag_kwargs.pop('bordered', self.bordered)
        striped = tag_kwargs.pop('striped', self.striped)
        table = Table(bordered=bordered, striped=striped, **tag_kwargs)
        if header:
            table.add(self.header())

        if isinstance(model_instances, (tuple, list)):
            for model in model_instances:
                table.add(self.row(model))
        else:
            table.add(self.row(model_instances))
        
        if tag is not None:
            tag.add(table)
            return tag.render(**kwargs)
        return table.render(**kwargs)



