"""
    proxies.utils
    ~~~~~~~~~~~~~
"""
from collections import OrderedDict

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
    
    def update(self, kwargs):
        """ Returns self instead of None on update to allow methods to be chained. """
        super().update(kwargs)
        return self
