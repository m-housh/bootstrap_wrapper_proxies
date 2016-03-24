"""
    proxies.extra
    ~~~~~~~~~~~~~
        
        Holds classes that I want to keep, but don't necessarily belong in this package.
"""
from functools import partial
from collections import namedtuple


class NamedTupleHelper:
    #:TODO: fix the doc strings with name change.
    """ NamedTupleHelper class is a namedtuple helper that allows us to combine fields from
        other NamedTupleHelper (namedtuple) instances to create new namedtuple's with fields
        from all the combined instances plus any fields we need to add to the tuple.
        Once combined (by default) all the values from the combined tuples are there,
        so we only need to add values to the fields that we added. My use case for this
        is using in conjunction with database Mixin's.  I'm able to define a key for
        the mixin and combine it with a key that use's that mixin, without having to
        remember/search for what the key should be for that mixin.  It is also used in
        SchemaKeyProxy which allows us to use uncommon names for db table columns but map
        them to more readable names. (See SchemaKeyProxy for more details.)
        
        :ex:
            >>> PersonKey = NamedTupleHelper('PersonKey', 'id','name')
            >>> p = PersonKey('Id', 'Name')
            >>> print(p)
            PersonKey(id='Id', name='Name')

            >>> EmployeeKey = NamedTupleHelper('EmployeeKey', 'employee_no', combines=(p,))
            >>> e = EmployeeKey('Employee Number')
            >>> print(e)
            EmployeeKey(employee_no='Employee Number', id='Id', name='Name')
    """
    
    #:TODO: allow combines to be instances of SchemaKeyProxy or SchemaLabelProxy.
    def __init__(self, name, *fields, combines=None):
        
        # the name of the namedtuple to create for the model
        self.name = name
        self._fields = list(fields)
        self.partial = None
        self.combines = combines
        self._instance = None

        if combines is not None:
            if isinstance(combines, (tuple, list)):
                self.partial = self._combine_tuples(self.name, self._fields, \
                        combines)
                # sets our _fields attr to the correct value
                self._fields = self._combine_fields(self._fields, combines)
            else:
                # raise error
                pass

    @classmethod
    def _combine_fields(cls, fields, *combines):
        """ Used to set the _fields on our insance to all of the fields from the combines
            that are passed in.  We store these fields on the instance so that a new/empty
            namedtuple can be created from the fields if needed.
        """
        if not isinstance(fields, list):
            fields = list(fields)
        if isinstance(combines, list) or isinstance(combines, tuple):
            for combo in combines:
                if hasattr(combo, '_fields'):
                    fields += [f for f in combo._fields if f not in fields]

        return fields


    @classmethod
    def _combine_tuples(cls, name, fields, combines):
        """ This method returns a new namedtuple with the name passed in.
            The :fields: should be a list of new fields to add above and beyond
            the tuples we combine.  The :combines: should be a list or tuple
            of namedtuples to combine together to make our new tuple.  This
            method will return a partial namedtuple with all the values from
            the combines already there, so that we only need to supply values
            for the new fields we are adding.
        """

        # fields should be a list or tuple of new fields to add to 
        # beyond the ones we are combining.
        if isinstance(fields, tuple):
            fields = list(fields)
        elif not isinstance(fields, list):
            # raise error
            pass

        if isinstance(combines, list) or isinstance(combines, tuple):
            # continue
            dct = {}
            for comb in combines:
                if hasattr(comb, '_fields'):
                    # update our fields list with the fields of the tuple
                    fields += list(comb._fields)
                    # update the values in our dct so we can return a 
                    # partial namedtuple with the values from our other
                    # classes.
                    dct.update(comb._asdict())

            # create a new namedtuple with all of our fields
            new_tuple = namedtuple(name, fields)
            
            # return a partial of our new tuple with the values from
            # the tuples we've combined.  This allows us to only have to 
            # specify values for any of the new fields we've added.
            return partial(new_tuple, **dct)

    @classmethod
    def _new_tuple(cls, name, fields):
        """ This allows to create a named tuple that is not a partial with all of 
            our needed fields. Can be useful if you want to specify a different value
            for field than the original key that got combined with this one.  The order
            of the fields is not garaunteed, so when instantiating a new tuple it is best
            to only use kwargs to do so.
                
                :ex:    
                        >>> IdKey = NamedTupleHelper('IdKey', 'id')
                        >>> idkey = IdKey('Id') # or IdKey(id='Id')
                        >>> NameKey = NamedTupleHelper('NameKey', 'name', combines=(idkey,))
                        >>> namekey = NameKey('Name') # or NameKey(name='Name')
                        >>> print(namekey)
                        NameKey(name='Name', id='Id')
                        >>> FreshKey = NameKey.new_tuple('FreshKey')
                        >>> fresh = FreshKey(id='Fresh Id', name='Fresh Name') # correct
                        >>> print(fresh)
                        FreshKey(name='Fresh Name', id='Fresh Id')
                        >>> fresh2 = FreshKey('Fresh Id', 'Fresh Name') # wrong
                        >>> print(fresh2)
                        FreshKey(name='Fresh Id', id='Fresh Name')
                        
        """
        return namedtuple(name, fields)
   
    def clean_tuple(self, name):
        """ Returns a new instance of NamedTupleHelper, with all the fields, but none of the 
            combined values. 
        """
        return NamedTupleHelper(name, *self._fields)

    def __repr__(self):
        return '<NamedTupleHelper: {}>'.format(self.name)

    def __call__(self, *args, **kwargs):
        """ Return a namedtuple populated with the *args, or **kwargs. 
            This allows us to use as follows.
            :ex:
                >>> S = NamedTupleHelper('S', 'id', 'name') # creates a namedtuple 'S' with fields 'id', 'name'
                >>> s = S('Id', 'Name')
                >>> print(s)
                S(id='Id', name='Name')
        """
        if self._instance is not None:
            self._instance = None

        if self.partial is not None:
            self._instance = self.partial(*args, **kwargs)
        else:
            new_tuple = self._new_tuple(self.name, self._fields)
            self._instance = new_tuple(*args, **kwargs)

        return self._instance


