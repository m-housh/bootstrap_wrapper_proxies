"""
    proxies.contexts.table_view_context
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from bootstrap_wrapper import Table, TableHeader, TableRow, ResponsiveTable
from .view_context import ViewContext

class TableViewContext(ViewContext):
    """ Renders a table or responsive table for a database model/ list of database models.
        This should be registered on a ModelViewProxy instance for a given database model.
        See tests for more details.
    """
    tag = ResponsiveTable
   
    def __init__(self, *args, responsive=True, bordered=False, striped=False, **kwargs):
        super().__init__(*args, **kwargs)
        # default is a responsive table, if not needed then this renders a table
        if not responsive:
            self.tag = Table
        # defaults for bordered or striped table, these can be overriden during a 
        # render call by passing them in as tag_kwargs.
        self.bordered = bordered
        self.striped = striped


    def header(self, **kwargs):
        """ Render's a table header based on the labels passed into this class upon 
            initialization. (Implementation is in ViewContext.)
        """
        return TableHeader(
            *self.labels.values(),
            **kwargs)

    
    def row(self, model_instance, *args, **kwargs):
        """ Creates a table row for a database model instance. """
        return TableRow(
            *[getattr(model_instance, key) for key in self.labels.keys()], 
            **kwargs)

    def render(self, model_instances=None, header=True, tag_kwargs=None, **kwargs):
        """ Renders a table or a responsive table element.
            
            :param model_instances: a single/list of database models to render as table row's
            :param header:          if True renders a table header if False does not render
                                    a table header.
            :param tag_kwargs:      kwargs to be passed to the table tag on instantiation
            :param kwargs:          kwargs to be passed to the tag's render method.
        """
        # just a placeholder if we are using responsive table this get's set to an
        # instance of a responsive table
        #:TODO: should make responsive be defined at a call to render, not instantiation of
        #       the class that would make this more flexible.
        tag = None
        if self.tag is ResponsiveTable:
            tag = self.tag()

        if tag_kwargs is not None:
            # make sure that kwargs is a dict
            if not isinstance(tag_kwargs, dict):
                # error
                try:
                    tag_kwargs = dict(tag_kwargs)
                except:
                    raise TypeError('tag_kwargs must be dict')
        else:
            # if no kwargs make an empty dict object.
            tag_kwargs = {}

               
        # get whether this table should be bordered and striped.  defaults can be set
        # at time this class was instantiatied but overriden by values passed in with
        # tag_kwargs in a render call.  This makes it easier to not have to register multiple
        # table view's with a ModelViewProxy instance.
        bordered = tag_kwargs.pop('bordered', self.bordered)
        striped = tag_kwargs.pop('striped', self.striped)
        # create our table instance.
        table = Table(bordered=bordered, striped=striped, **tag_kwargs)
        if header is True:
            # add a header row to our table
            table.add(self.header())
        
        # not sure why you would not pass at least one instance into the render call, but
        # hey if you want a blank table/ you can have one.
        if model_instances is not None:
            # check whether we have many model's or just one.
            if isinstance(model_instances, (tuple, list)):
                for model in model_instances:
                    # add a table row for each model
                    table.add(self.row(model))
            else:
                # add a table row for just one model
                table.add(self.row(model_instances))
        # if we are rendering an instance of ResponsiveTable tag will not be None 
        if tag is not None:
            # if responsive add our table
            tag.add(table)
            # render a responsive table
            return tag.render(**kwargs)
        # else render a non-responsive table
        return table.render(**kwargs)



