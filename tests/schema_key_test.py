from unittest import TestCase

from proxies.schema_key import SchemaKey

Key = SchemaKey('Key', 'id', 'name')
key = Key('Id', 'Name')

class SchemaKeyTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)

    def test_attributes(self):
        AKey = SchemaKey('AKey', 'id', 'name')
        self.assertEqual(AKey.name, 'AKey')
        self.assertListEqual(AKey._fields, ['id', 'name'])
        self.assertIsNone(AKey.partial)
        self.assertIsNone(AKey.combines)
        self.assertIsNone(AKey._instance)

    def test_call(self):
        key = Key('Id', 'Name')
        self.assertTupleEqual(key, ('Id', 'Name'))


    def test_combines(self):
        AnotherKey = SchemaKey('AnotherKey', 'another', combines=(key,))
        a = AnotherKey('Another')
        self.assertTupleEqual(a, ('Another', 'Id', 'Name'))

    def test_combine_fields_on_non_list(self):
        X = SchemaKey('X', 'x',)
        x = X('X')
        print('x._fields', x._fields)
        y = SchemaKey._combine_fields([], x, key)
        self.assertListEqual(y, ['x', 'id','name'])

    def test_new_tuple(self):
        NewKey = Key.new_tuple('NewKey', Key._fields)
        new_key = NewKey('New Id','New Name')
        self.assertTupleEqual(new_key, ('New Id', 'New Name'))
