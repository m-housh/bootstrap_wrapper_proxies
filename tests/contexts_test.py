from unittest import TestCase

from proxies import BaseViewContext, OrderedLabels, TableViewContext, SchemaLabelProtocol, \
        ModelViewProxy
from bootstrap_wrapper import Table, TableHeader, TableRow, ResponsiveTable

class Model(SchemaLabelProtocol):
    labels = { 'id': 'Id', 'name': 'Name', 'email': 'Email' }

    def __init__(self):
        self.id = 12345
        self.name = 'Michael'
        self.email = 'test@test.com'

model_view = ModelViewProxy(Model)

class ContextsTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    # this should move to core tests
    def test_render_raises_error_in_view_context_if_not_implemented(self):
        v = BaseViewContext()
        try:
            v.render()
        except NotImplementedError as e:
            self.assertIsNotNone(e)


    def test_table_view_context(self):
        model = Model()
        model_view.register_context('table', TableViewContext, 
                label_order={'name': 0, 'id': -1 }, responsive=False)

        test_v = Table(TableHeader(
            *(Model.labels['name'], Model.labels['email'], Model.labels['id'])),
            TableRow(model.name, model.email, model.id))
        
        tv = test_v.render()
        mv = model_view.render('table', model)

        self.assertEqual(mv, tv)
        
        # test that kwargs get passed on
        tv = test_v.render(inline=True)
        mv = model_view.render('table', model, inline=True)
        self.assertEqual(mv, tv)
        
        # test responsive table works this is the default setting for TableViewContext
        model_view.register_context('table-responsive', TableViewContext, 
                label_order={'name': 0, 'id': -1})
        r_test_v = ResponsiveTable(test_v)
        tv = r_test_v.render()
        mv = model_view.render('table-responsive', model)

        self.assertEqual(mv, tv)

        # test header doesn't get rendered
        test_v = Table(TableRow(
            model.name, model.email, model.id))
        tv = test_v.render()
        mv = model_view.render('table', model, header=False)
        self.assertEqual(mv, tv)



