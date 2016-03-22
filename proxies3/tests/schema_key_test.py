from unittest import TestCase

from proxies.schema_key import SchemaKey, SchemaMap, SchemaLabelProtocol

id_key = SchemaKey(id='Id')
person_key = SchemaKey(fn='First Name', ln='Last Name')

person_map = SchemaMap(id_key, person_key)
child_map = person_map.new_child()

class SchemaMapTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_chained_keys(self):
        self.assertEqual(person_map['id'], id_key['id'])
        self.assertEqual(person_map['fn'], person_key['fn'])
        self.assertEqual(person_map['ln'], person_key['ln'])


    def test_base_changes_reflected_on_chained_instance(self):
        t_id = id_key.copy()
        t_person = person_key.copy()

        t_map = SchemaMap(t_id, t_person)
        self.assertEqual(t_map['id'], 'Id')

        t_id['id'] = 'New Id'
        self.assertEqual(t_map['id'], 'New Id')


    def test_changes_in_map_dont_reflect_on_base_dicts(self):
        t_map = person_map.new_child()
        self.assertEqual(t_map['id'], id_key['id'])

        t_map['id'] = 'New Id'
        self.assertEqual(t_map['id'], 'New Id')
        self.assertNotEqual(t_map['id'], id_key['id'])

    def test_base_changes_filter_to_child_map(self):
        old_id = id_key['id']
        id_key['id'] = 'New Id'
        self.assertEqual(child_map['id'], 'New Id')

        id_key['id'] = old_id

class Labels(SchemaLabelProtocol):
    _labels = SchemaMap(person_key, id_key)

class SchemaLabelProtocolTestCase(TestCase):

    def test_labels_errors_if_not_implemented(self):

        try:
            class Test(SchemaLabelProtocol):
                pass
        except Exception as e:
            self.assertIsNotNone(e)


    def test_labels_in_context(self):
        class NewLabels(Labels):
            _labels = Labels.labels.new_child().update({'id': 'New Id', \
                    'fn': 'New First Name', 'ln': 'New Last Name'})


        self.assertEqual(NewLabels.labels['id'], 'New Id')
        self.assertNotEqual(Labels.labels['id'], NewLabels.labels['id'])
        

    def test_labels_without_context(self):
        class Test(Labels):
            pass

        self.assertEqual(Test.labels, Labels.labels)
        # updates on Test show up in Labels since they reference the same object
        Test.labels.update({'id': 'Test Id'})
        self.assertEqual(Labels.labels['id'], 'Test Id')

    
    def test_schema_label_meta_transforms_dict_to_schema_map(self):
        class Test(SchemaLabelProtocol):
            _labels = {'id': 'Id'}
        t = Test()

        self.assertIsInstance(t.labels, SchemaMap)
