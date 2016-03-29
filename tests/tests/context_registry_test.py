from unittest import TestCase

from inspect import isgenerator

from proxies.context_registry import ContextContainer, InvalidContextError, ContextRegistry
from proxies.core import BaseViewContext

class ContextRegistryTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_invalid_context(self):
        self.assertRaises(InvalidContextError, ContextRegistry, 'default', 'invalid')
        r = ContextRegistry()
        self.assertEqual(r.contexts, [])

    def test_registry_with_valid_context(self):
        # with a default key
        r = ContextRegistry('default', BaseViewContext)
        self.assertIsNotNone(r.get('default'))
        # without a key get's set to default and context works as class or instance
        r = ContextRegistry(BaseViewContext(model={}, labels={}))
        self.assertIsNotNone(r.get('default'))
        self.assertIsNone(r.get('fail'))

        r = ContextRegistry(key='default', context=BaseViewContext)
        self.assertIsNotNone(r.get('default'))

    def test_dot_style_access(self):
        r = ContextRegistry(BaseViewContext)
        self.assertIsNotNone(r.default)
        self.assertRaises(AttributeError, lambda: r.fails)

    def test_dict_style_access(self):
        r = ContextRegistry()
        r['default'] = BaseViewContext
        self.assertIsNotNone(r.get('default'))
        self.assertRaises(KeyError, lambda: r['fails'])
        self.assertEqual(r['default'], r.get('default'))
        self.assertRaises(InvalidContextError, r.__setitem__, 'fails', None)

    def test_keys_method(self):
        r = ContextRegistry(BaseViewContext)
        r['a'] = BaseViewContext
        r['b'] = BaseViewContext
        self.assertTupleEqual(r.keys(), ('default', 'a', 'b'))
        self.assertIsInstance(r.keys('list'), list)
        self.assertIsInstance(r.keys(list), list)
        self.assertTrue(isgenerator(r.keys(None)))

    def test_values_method(self):
        r = ContextRegistry(BaseViewContext)
        r['a'] = BaseViewContext
        r['b'] = BaseViewContext
        self.assertTupleEqual(r.values(), (BaseViewContext, BaseViewContext, BaseViewContext))
        self.assertIsInstance(r.values('list'), list)
        self.assertIsInstance(r.values(list), list)
        self.assertTrue(isgenerator(r.values(None)))

    def test_setitem_on_existing_key_removes_item_for_key(self):
        r = ContextRegistry(BaseViewContext)
        class TestViewContext(BaseViewContext):
            pass

        r['default'] = TestViewContext
        self.assertEqual(r['default'], TestViewContext)
        self.assertEqual(len(r.contexts), 1)


