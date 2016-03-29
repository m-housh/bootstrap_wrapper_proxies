from unittest import TestCase

from proxies.model_view import BaseModelViewProxy, ModelViewProxy
from proxies.schema_helper import SchemaLabelProtocol
from proxies.core import BaseViewContext, BaseErrorHandler
from proxies.context_registry import ContextRegistry, InvalidContextError

class Labeled(SchemaLabelProtocol):
    labels = {'id': 'Id', 'fn': 'First Name', 'ln': 'Last Name'}

class NotLabeled:
    pass

class TestViewContext(BaseViewContext):
    def render(self, *args, **kwargs):
        return 'It Worked'



class BaseModelViewProxyTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_attributes(self):
        m = BaseModelViewProxy(Labeled)
        self.assertEqual(m.model_class, Labeled)
        self.assertEqual(m.labels, Labeled.labels)

        m = BaseModelViewProxy(Labeled())
        self.assertEqual(m.model_class, Labeled)
        self.assertEqual(m.labels, Labeled.labels)


    def test_error_raised_if_class_is_not_schema_label_protocol(self):
        self.assertRaises(TypeError, BaseModelViewProxy, NotLabeled)
        self.assertRaises(TypeError, BaseModelViewProxy, NotLabeled())

    def test_register_context_method(self):
        m = BaseModelViewProxy(Labeled)
        m.register_context('table', 'default', TestViewContext)
        self.assertEqual(m.registerys['table'].get('default'), TestViewContext)
        self.assertIsInstance(m.registerys['table'], ContextRegistry)
        t = TestViewContext(model={}, labels={})
        m.register_context('test', 'default', t)
        self.assertEqual(m.registerys['test'].get('default'), t)

        self.assertRaises(InvalidContextError, m.register_context, \
                'test1', 'default', NotLabeled)
        n = NotLabeled()
        self.assertRaises(InvalidContextError, m.register_context, \
                'test2', 'default', n)
        m.register_context('table', 'responsive', TestViewContext)
        self.assertTupleEqual(m.registerys['table'].values(), 
                (TestViewContext, TestViewContext))

    def test_get_context_method(self):
        m = BaseModelViewProxy(Labeled)
        m.register_context('table', 'default', TestViewContext)

        self.assertEqual(m.get_context('table'), m.registerys.table)
        self.assertEqual(m.get_context('table.default'), TestViewContext)
        self.assertEqual(m.get_context('table', 'default'), TestViewContext)

        self.assertRaises(ValueError, m.get_context, 'table', 'default', 'fail')
        self.assertRaises(ValueError, m.get_context)
        self.assertRaises(KeyError, m.get_context, 'fail')
        self.assertRaises(KeyError, m.get_context, 'table', 'fail')

    def test_init_context_method(self):
        m = BaseModelViewProxy(Labeled)
        m.register_context('test', 'default', TestViewContext)
        context = m.init_context('test', 'default', label_order={'fn': 0, 'id': -1})
        self.assertIsInstance(context, TestViewContext)
        self.assertDictEqual({'id': 'Id','fn': 'First Name', 'ln': 'Last Name'}, 
                context.labels)
        self.assertEqual(context.model, Labeled)
        self.assertEqual(m.render(context), 'It Worked')
        
        m.register_context('test', 'instance', context)
        new_instance = m.init_context('test', 'instance')
        self.assertIsInstance(new_instance, TestViewContext)
        self.assertNotEqual(context, new_instance)
    
    def test_render_method(self):
        m = BaseModelViewProxy(Labeled)
        m.register_context('test', 'default', TestViewContext)
        # will call init on a context if it's a class
        self.assertEqual(m.render(m.get_context('test.default')), 'It Worked')
         
        context = m.init_context('test', 'default', label_order={'fn': 0, 'id': -1})
        # also works on an instance
        self.assertEqual(m.render(context), 'It Worked')
        count = 0
        for k, v in context.labels.items():
            if count == 0 and k != 'fn':
                print(context.labels)
                raise Exception(count)
            if count == 1 and k != 'ln':
                print(context.labels)
                raise Exception(count)
            if count == 2 and k != 'id':
                print(context.labels)
                raise Exception(count)

            count += 1

        # with a string and dot style syntax
        self.assertEqual(m.render('test.default'), 'It Worked')
        # if have a default key registered it will work without dot style syntax
        self.assertEqual(m.render('test'), 'It Worked')
        
        # raises key error if not in contexts
        self.assertRaises(KeyError, m.render, 'fail')
        # raises key error if invalid sub-context
        self.assertRaises(KeyError, m.render, 'test.fail')

        m.register_context('another', 'not_default', context) # reusing context from earlier
        # raises value error on invalid sub-key with no default registered
        self.assertRaises(ValueError, m.render, 'another')
        self.assertRaises(ValueError, m.render, 'another.too.many.keys')

class ModelViewProxyTestCase(TestCase):

    def test_init_errors_get_handled(self):
        self.assertRaises(TypeError, ModelViewProxy, None, BaseErrorHandler())
        
    def test_register_context_errors_get_handler(self):
        m = ModelViewProxy(Labeled, BaseErrorHandler()) 
        self.assertRaises(InvalidContextError, m.register_context, 'test', 'default', {})

    def test_get_context_errors_get_handled(self):
        m = ModelViewProxy(Labeled, BaseErrorHandler()) 
        self.assertRaises(KeyError, m.get_context, 'test', 'default')

    def test_init_context_errors_get_handled(self):
        m = ModelViewProxy(Labeled, BaseErrorHandler()) 
        self.assertRaises(KeyError, m.init_context, 'test', 'default')

    def test_render_errors_get_handler(self):
        m = ModelViewProxy(Labeled, BaseErrorHandler()) 
        self.assertRaises(KeyError, m.render, 'test', 'default')

    def test_we_get_a_base_error_handler_if_not_passed_in(self):
        m = ModelViewProxy(Labeled) 
        self.assertIsInstance(m.error_handler, BaseErrorHandler)



