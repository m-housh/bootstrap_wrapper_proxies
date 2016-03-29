"""
    proxies.utils
    ~~~~~~~~~~~~~
"""
from collections import OrderedDict
from functools import wraps

class OrderedLabels(OrderedDict):
    """ An ordered dict object responsible for sorting labels into the correct order
        to be used inside a view context.  The passed labels keys should map to the
        passed in order_kwargs keys.  If you don't care about the order of certain keys
        they don't need to be in the order_kwargs.  The keys not found in the order_kwargs
        will be placed between the highest positve and the lowest negative number in 
        the order_kwargs.  Order_kwargs values can be positive or negative numbers with
        the first item in the dictionary being item 0 and the last item being item -1 and 
        second to last being item -2 and so on. This is helpful when you only care about
        moving a certain key to the end of the order.
    """
    def __init__(self, labels, order_kwargs):
        if len(order_kwargs) > 0:
            # get all the orders that are negative numbers
            negatives = sorted([ (k, v) for k, v in order_kwargs.items() if v < 0 ])
            # get all the orders that are positve numbers
            positives = sorted([ (k, v) for k, v in order_kwargs.items() if v >= 0 ])
            # combine the keys that are already accounted for in the lists
            accounted_for_keys = [ k[0] for k in negatives ] + [ k[0] for k in positives ]
            # check for any left over keys and add them to the positives
            for key in labels.keys():
                if key not in accounted_for_keys:
                    positives.append((key, positives[-1][1] + 1))
            # initialize an ordered dict with the key,values in the right order
            super().__init__([ (k, labels[k]) for k, _ in positives + negatives ])
        super().__init__(labels)
    
    def update(self, kwargs):
        """ Returns self instead of None on update to allow methods to be chained. """
        super().update(kwargs)
        return self



class TypeParser:

    def __init__(self, type):
        self.type = type

    def __call__(self, args, return_type=None):
        """ return a generator(default), list, or a tuple  for the type. """
        
        r_type = {
                'list': lambda v: list(v),
                'tuple': lambda v: tuple(v) }.get(return_type, return_type)

        r_value = (t for t in args if isinstance(t, self.type))
        if r_type is None:
            # return a generator if no return_type passed in
            return r_value
        return r_type(r_value)


def get_first(f):
    """ helper to get the first of a type or return None if none were found """
    @wraps(f)
    def get_first_wrapper(args):
        try:
            return next(f(args))
        except StopIteration:
            return None
    
    return get_first_wrapper

