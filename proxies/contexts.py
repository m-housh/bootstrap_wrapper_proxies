"""
    proxies3.proxies.contexts
    ~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from .core import BaseViewContext

class TableViewContext(BaseViewContext):

    def header_row(self):
        pass

    def table_row(self):
        pass

