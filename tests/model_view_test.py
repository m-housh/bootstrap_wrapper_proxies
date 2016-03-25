from unittest import TestCase

from proxies import SchemaLabelProtocol, ModelViewProxy, BaseViewContext


class Labeled(SchemaLabelProtocol):
    labels = {'id': 'Id'}

class NotLabeled:
    pass


my_model_view = ModelViewProxy(Labeled)

class ModelViewTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_error_raised_for_class_that_does_not_implement_schema_label_protocol(self):
        try:
            model_view = ModelViewProxy(NotLabeled)
        except TypeError as e:
            self.assertIsNotNone(e)

    def test_does_not_error_for_class_or_instance_that_implements_schema_label_protocol(self):
        self.assertIsNotNone(my_model_view.model_class)
        self.assertEqual(my_model_view.model_class, Labeled) 

        labeled = Labeled()
        model_view2 = ModelViewProxy(labeled)
        self.assertEqual(model_view2.model_class, Labeled)

    def test_model_view_attributes(self):
        self.assertEqual(my_model_view.labels, Labeled.labels)
        self.assertEqual(my_model_view.model_class, Labeled)

        # test that the model_view get's it's own context for labels
        # I'm rethinking a new context at the model_view level.  I feel the new
        # context should be at the context level, so that a model view will inherit
        # all changes made to base class's but any override in a view context will
        # only affect that view context, so commenting out the next part of this test

        #my_model_view.labels.update({'id': 'New Id'})
        #self.assertNotEqual(Labeled.labels['id'], my_model_view.labels['id'])

        self.assertEqual(my_model_view._view_ctx['labels'], my_model_view.labels)
    
    def test_register_context_method_raises_error_if_context_not_dict(self):
        try:
            my_model_view.register_context('form', ())
        except TypeError as e:
            self.assertIsNotNone(e)

    def test_register_context_errors_without_render_method(self):
        try:
            my_model_view.register_context('form', {'key': 'value'})
        except TypeError as e:
            self.assertIsNotNone(e)

    def test_render_method_raises_error_if_context_not_available(self):
        try:
            my_model_view.render('error')
        except KeyError as e:
            self.assertIsNotNone(e)

    def test_get_render_for_context_method(self):
        new_view = ModelViewProxy(Labeled)
        try:
            new_view.render('table')
        except KeyError as e:
            self.assertIsNotNone(e)

    '''
    This needs updated because context requires a context class
    def test_render_method_on_valid_context(self):
        # add a render method to our form context
        my_model_view.register_context('form', { 'render': lambda: 'It works' })
        self.assertEqual(my_model_view.render('form'), 'It works')
    '''

