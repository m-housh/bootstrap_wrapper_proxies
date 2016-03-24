from unittest import TestCase

from proxies import BaseViewContext, OrderedLabels

class ContextsTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)


    def test_render_raises_error_in_view_context_if_not_implemented(self):
        v = BaseViewContext()
        try:
            v.render()
        except NotImplementedError as e:
            self.assertIsNotNone(e)


