from unittest import TestCase

from proxies.schema_helper import SchemaKey, SchemaMap, SchemaLabelProtocol

id_key = SchemaKey(id='Id')
person_key = SchemaKey(fn='First Name', ln='Last Name')

person_map = SchemaMap(id_key, person_key)
child_map = person_map.new_child()

class Labels(SchemaLabelProtocol):
    labels = SchemaMap(person_key, id_key)


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


class SchemaLabelProtocolTestCase(TestCase):

    def test_labels_errors_if_not_implemented(self):
        error = None
        try:
            class Test(SchemaLabelProtocol):
                pass
        except Exception as e:
            error = e

        self.assertIsNotNone(error)

    def test_labels_in_context(self):
        class NewLabels(Labels):
            labels = Labels.labels.new_child().update({'id': 'New Id', \
                    'fn': 'New First Name', 'ln': 'New Last Name'})
        self.assertEqual(NewLabels.labels['id'], 'New Id')
        self.assertNotEqual(Labels.labels['id'], NewLabels.labels['id'])
        

    def test_subclasses_get_new_context(self):
        class Test(Labels):
            pass

        self.assertEqual(Test.labels, Labels.labels)
        # if updated outside of class they get pushed to new context
        Test.labels.update({'id': 'Test Id'})
        self.assertEqual(Labels.labels['id'], 'Id')

        class Test1(SchemaLabelProtocol):
            labels = SchemaMap(Labels.labels)
        
        # wrong way to update
        class Test2(Test):
            labels = Test1.labels.update({'id': 'Test2 Id'})

        self.assertEqual(Test1.labels['id'], Test2.labels['id'])

        class Test3(Test2):
            pass
        
        # right way or use new_child (see test_labels_in_context test.)
        Test3.labels.update({'id': 'Test3 Id'})
        self.assertNotEqual(Test3.labels['id'], Test2.labels['id'])
    
    def test_schema_label_meta_transforms_dict_to_schema_map(self):
        class Test(SchemaLabelProtocol):
            labels = {'id': 'Id'}

        self.assertIsInstance(Test.labels, SchemaMap)

    def test_changes_reflect_if_made_on_base_context(self):
        #class Test(SchemaLabelProtocol):
        #    labels = {'id': 'Id'}

        class Test(SchemaLabelProtocol):
            """ Mock to show that as long as label is updated at class it get's reflected
                to sub-classes.
            """
            labels = {'id': 'New Id'}

        class Test1(Test):
            labels = SchemaKey({'fn': 'First Name'})

        class Test2(Test1):
            labels = {'ln': 'Last Name'}

        # this is for commented out Test class.
        #self.assertDictEqual({'id': 'Id', 'fn': 'First Name', 'ln': 'Last Name'}, \
                #dict(Test2.labels))
        
        # this doesn't work becaus the class get's a new context after initiated
        #Test.labels.update({'id': 'New Id'})

        self.assertEqual(Test2.labels['id'], 'New Id')
        # if updated after class creation it doesn't reflect on sub-classes
        Test.labels.update({'id': 'Id'})
        self.assertNotEqual(Test2.labels['id'], Test.labels['id'])
