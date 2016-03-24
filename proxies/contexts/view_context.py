"""
    proxies.contexts
    ~~~~~~~~~~~~~~~~
"""
from proxies.core import BaseViewContext
from proxies.utils import OrderedLabels

from bootstrap_wrapper import Div
from inspect import isclass

class ViewContext(BaseViewContext):
    """ A view context wrapper around an bootstrap_wrapper html_tag. """
    tag = Div
    label_order = None

    def __init__(self, *args, model=None, labels=None, label_order=None, **kwargs):
        self.model = model
        self.label_order = label_order or {}
        if labels is None:
            labels = {}

        self.labels = OrderedLabels(labels, self.label_order)
        
        # this should probably be moved to a meta class
        if not isclass(self.tag):
            self.tag = self.tag.__class__

    def render(self, *args, tag_kwargs=None, **kwargs):
        if not tag_kwargs:
            tag_kwargs = {}

        tag = self.tag(**tag_kwargs)

        return tag.render(*args, **kwargs)
