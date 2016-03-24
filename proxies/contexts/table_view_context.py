"""
    proxies.contexts.table_view_context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from bootstrap_wrapper import Table, TableHeader, TableRow, ResponsiveTable
from .view_context import ViewContext

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
                raise TypeError('tag_kwargs must be dict')
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



