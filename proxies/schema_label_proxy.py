"""
    proxies.schema_label_proxy
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        Holds our SchemaLabelProxy class.  Which is used to map db.Model schema attributes
        to human readable labels to be used in views. Although not required by this Proxy
        most models that implement this should also implement SchemaKeyProxy.
"""

class SchemaLabelProxy:
    """ Assures that models that live up to this proxy implement a labels method. 
        The labels method should return a SchemaKey object (or namedtuple) with Human 
        readable values to be used inside of views.  The _fields attribute of the named tuple
        should be mapped to attributes of the model it is for.

        :ex:
            from proxies import SchemaKey, SchemaKeyProxy, SchemaLabelProxy
            

            # NOTE: Make sure that SchemaKeyProxy is to the left of db.Model
            #       or you will get TypeError: invalid keyword argument from 
            #       sqlalchemy's _declaritive_constructor.
            # Now this is working no matter the placement, but leaving note encase it
            # happens again

            class SimplePerson(SchemaKeyProxy, SchemaLabelProxy, db.Model):
                id = db.Column(db.Integer, primary_key=True)
                fn = db.Column(db.String)
                ln = db.Column(db.String)
                
                @classmethod
                def key(cls):
                    # SchemaKeyProxy gives us access to variables with non-human friendly
                    # names in a human readable way. (See SchemaKeyProxy for details.)
                    SimplePersonKey = SchemaKey('SimplePersonKey', 'id', 'fn', 'ln')
                    return SimplePersonKey('id', 'firstname', 'lastname')

                @classmethod
                def labels(cls):
                    # easiest to use the new_tuple method of the SchemaKey object returned
                    # from self.key method, unless multiple combines are used then it's
                    # easier to use the SchemaKey class itself.
                    SimplePersonLabels = self.key().new_tuple('SimplePersonLabels')

                    # however this could also be done with
                    # SimplePersonLabels = SchemaKey('SimplePersonLabels', 'id','fn', 'ln')
                    
                    # :NOTE: SchemaKey.new_tuple does not always retain order, if the
                    #       key is made up of different combined SchemaKey objects, so it is
                    #       best to use kwargs to set values for keys in the namedtuple.
                    
                    return SimplePersonLabels(id='Id', fn='First Name', ln='Last Name')

                
                >>> print(SimplePerson.labels())
                SimplePersonLabels(id='Id', fn='First Name', ln='Last Name'

    """
    @classmethod
    def labels(cls):
        raise NotImplementedError


