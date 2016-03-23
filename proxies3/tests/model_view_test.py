from unittest import TestCase

from proxies import SchemaLabelProtocol, ModelView


class Labeled(SchemaLabelProtocol):
    labels = {'id': 'Id'}

class NotLabeled:
    pass


my_model_view = ModelView(Labeled)

class ModelViewTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_error_raised_for_class_that_does_not_implement_schema_label_protocol(self):
        try:
            model_view = ModelView(NotLabeled)
        except TypeError as e:
            self.assertIsNotNone(e)

    def test_does_not_error_for_class_or_instance_that_implements_schema_label_protocol(self):
        self.assertIsNotNone(my_model_view._model_class)
        self.assertEqual(my_model_view._model_class, Labeled) 

        labeled = Labeled()
        model_view2 = ModelView(labeled)
        self.assertEqual(model_view2._model_class, Labeled)

    def test_model_view_attributes(self):
        self.assertEqual(my_model_view.labels, Labeled.labels)
        # test that the model_view get's it's own context for labels
        my_model_view.labels.update({'id': 'New Id'})
        self.assertNotEqual(Labeled.labels['id'], my_model_view.labels['id'])
    

