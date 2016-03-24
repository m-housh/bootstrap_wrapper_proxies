"""
    proxies.contexts
    ~~~~~~~~~~~~~~~~
"""
from .core import BaseViewContext

class ViewContext(BaseViewContext):
    """ A view context wrapper around an bootstrap_wrapper html_tag. """
    def __init__(self, html_tag, *args, **kwargs):
        self.tag = html_tag

    def add(self, *args, **kwargs):
        return self.tag.add(*args, **kwargs)

    def render(self, *args, **kwargs):
        return self.tag.render(*args, **kwargs)
