from unittest import TestCase

from proxies import TableViewContext, SchemaLabelProtocol, ModelViewProxy
from bootstrap_wrapper import Table, TableHeader, TableRow, ResponsiveTable
from copy import deepcopy

class Model(SchemaLabelProtocol):
    labels = { 'id': 'Id', 'name': 'Name', 'email': 'Email' }

    def __init__(self):
        self.id = 12345
        self.name = 'Michael'
        self.email = 'test@test.com'

model_view = ModelViewProxy(Model)
model_view.register_context('table', TableViewContext, label_order={'name': 0, 'id': -1},
        responsive=False)
model_view.register_context('table-responsive', TableViewContext, 
        label_order={'name': 0, 'id': -1 })
model_view.register_context('table-bordered-striped', TableViewContext, 
        label_order={'name': 0, 'id': -1}, bordered=True, striped=True, responsive=False)

model = Model()
model2 = Model()

test_table = Table(TableRow(
    model.name, model.email, model.id))

test_table_with_header = Table(TableHeader(
    Model.labels['name'], Model.labels['email'], Model.labels['id']),
    TableRow(model.name, model.email, model.id))

class TableViewContextTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_responsive_no_header(self):
        mv = model_view.render('table-responsive', model, header=False)
        tv = ResponsiveTable(test_table).render()
        self.assertEqual(mv, tv)

    def test_responsive_with_header(self):
        mv = model_view.render('table-responsive', model)
        tv = ResponsiveTable(test_table_with_header).render()
        self.assertEqual(mv, tv)

    def test_render_kwargs_get_passed_through(self):
        mv = model_view.render('table', model, pretty=True)
        tv = test_table_with_header.render(pretty=True)
        self.assertEqual(mv, tv)

    def test_render_with_list_of_model_instances(self):
        test = deepcopy(test_table)
        test.add(TableRow(model2.name, model2.email, model2.id))

        mv = model_view.render('table', [model, model2], header=False)
        tv = test.render()
        self.assertEqual(mv, tv)


    def test_render_with_tag_kwargs_raises_error_if_not_dict(self):
        self.assertRaises(TypeError, model_view.render, 'table', model, tag_kwargs=())

    def test_render_with_tag_kwargs(self):
        test = deepcopy(test_table)
        test.attributes.update({'style': 'somestyle'})

        mv = model_view.render('table', model, header=False, tag_kwargs={'style':'somestyle'})
        tv = test.render()

        self.assertEqual(mv, tv)

    def test_bordered_and_striped(self):
        test = deepcopy(test_table)
        test.attributes.update({'class': 'table table-bordered table-striped'})
        mv = model_view.render('table-bordered-striped', model, header=False)
        tv = test.render()
        self.assertEqual(mv, tv)

    def test_bordered_and_striped_can_be_overridden(self):
        test = deepcopy(test_table)
        test.attributes.update({'class': 'table table-striped'})
        mv = model_view.render('table-bordered-striped', model, header=False, 
                tag_kwargs={'bordered': False})
        tv = test.render()
        self.assertEqual(mv, tv)

