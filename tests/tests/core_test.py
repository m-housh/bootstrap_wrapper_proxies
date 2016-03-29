from unittest import TestCase
from proxies.core import BaseDict, BaseViewContext

class BaseDictTestCase(TestCase):

    def test_update_returns_self(self):
        b = BaseDict()
        c = b.update({'id': 'something'})
        self.assertEqual(c, b)
        self.assertDictEqual(c, {'id': 'something'})

    def test_dot_style_access_to_keys(self):
        b = BaseDict({'id': 'something'})
        self.assertEqual(b.id, 'something')

        self.assertRaises(AttributeError, lambda: b.fails)


class BaseViewContextTestCase(TestCase):

    def test_base_view_context(self):
        b = BaseViewContext(model=BaseDict, labels={'id': 'Id'}, label_order={'id': -1})
        self.assertRaises(NotImplementedError, b.render)
        self.assertRaises(ValueError, BaseViewContext, model=None)
        b = BaseViewContext(model={})
        self.assertEqual(b.labels, {})
