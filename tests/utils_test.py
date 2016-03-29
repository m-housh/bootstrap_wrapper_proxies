from unittest import TestCase

from proxies.utils import *
from proxies.core import BaseDict

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

class ParsingUtilsTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)

    def test_base_parser(self):
        string_parser = TypeParser(str)
        strings = string_parser(('a','b','c'), list)
        self.assertListEqual(['a','b','c'], strings)
        s2 = string_parser(('a','b','c'), list)
        self.assertListEqual(['a','b','c'], strings)
        s3 = string_parser(('a','b','c'), tuple)
        self.assertTupleEqual(('a','b','c'), s3)

        s4 = string_parser(('a','b','c', (), {}, []))

        a = next(s4)
        b = next(s4)
        c = next(s4)

        self.assertEqual(a, 'a')
        self.assertEqual(b, 'b')
        self.assertEqual(c, 'c')

        self.assertRaises(StopIteration, next, s4)


    def test_get_first(self):
        get_first_string = get_first(TypeParser(str))
        a = get_first_string(('a','b','c', {}, [], ()))
        self.assertEqual(a, 'a')
        
        none = get_first_string(({}, [], ()))
        self.assertIsNone(none)

