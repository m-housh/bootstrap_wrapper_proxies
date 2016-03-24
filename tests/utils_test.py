from unittest import TestCase

from proxies import OrderedLabels

labels = {'fn': 'First Name','id': 'Id', 'email': 'Email', 'ln': 'Last Name'}

class UtilTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_ordered_labels(self):
        ordered = OrderedLabels(labels, {'fn': 0, 'ln': 1,  'id': -1 , 'email': -2})
        count = 0
        for k, v in ordered.items():
            print(k, v, count)
            if count == 0:
                self.assertEqual(k, 'fn')
            if count == 1:
                self.assertEqual(k, 'ln')
            if count == 2:
                self.assertEqual(k, 'email')
            if count == 3:
                self.assertEqual(k, 'id')

            count += 1


    def test_ordered_labels_update_returns_self(self):
        ordered = OrderedLabels(labels, {'fn': 0, 'ln': 1})
        self.assertEqual(ordered.update({'id': 'Edit'}), ordered)

