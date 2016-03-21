"""
    db.schema_key_proxy
    ~~~~~~~~~~~~~~~~~~~

    A proxy for a model schema key and helpers.
"""

class SchemaKeyProxy:
    """ key method should return a SchemaKey object with values mapped to attributes of
        the model it used for.  This allows us to have different keys in the database
        versus the keys we use to access attributes on our model, if applicable.  
           
        :ex:
            from proxies import SchemaKey, SchemaKeyProxy
            

            # NOTE: Make sure that SchemaKeyProxy is to the left of db.Model
            #       or you will get TypeError: invalid keyword argument from 
            #       sqlalchemy's _declaritive_constructor.
            # Now this is working no matter the placement, but leaving note encase it
            # happens again

            class SimplePerson(SchemaKeyProxy, db.Model):
                id = db.Column(db.Integer, primary_key=True)
                fn = db.Column(db.String)
                ln = db.Column(db.String)
                
                @classmethod
                def key(cls):
                    SimplePersonKey = SchemaKey('SimplePersonKey', 'id', 'fn', 'ln')
                    return SimplePersonKey('id', 'firstname', 'lastname')

            #>>> bob = SimplePerson(firstname='Bob', lastname='Hope')
            #>>> print(b.fn)
            #Bob
            #>>> print(b.firstname)
            #Bob

        This can actuall be implemented when declaring a table column on a model, but
        didn't realize that until after I created this (with exception to enforcing a model 
        class has the key method).

            ex: id = db.Column('user_id',...)   # which would map id on our class to user_id
                                                # in the database.

        
    """

    def __init__(self, **kwargs):
        if kwargs:
            for key in kwargs.keys():
                self.__setitem__(key, kwargs[key])

    @classmethod
    def key(cls):
        raise NotImplementedError

    def _prepare_key(self, key):
        if key in self.key():
            index = self.key().index(key)
            return self.key()._fields[index]

        return key

    def __getattr__(self, key):
        return self.__dict__.get(self._prepare_key(key))

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.__dict__.update({self._prepare_key(key): value})
            
    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        del(self.__dict__[self._prepare_key(key)])
