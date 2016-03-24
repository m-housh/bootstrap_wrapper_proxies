from unittest import TestCase

from proxies import ViewContext, LabelOrder

class ContextsTestCase(TestCase):

    def test_sanity(self):
        self.assertEqual(2, 2)
        self.assertNotEqual(2, 3)


    def test_render_raises_error_in_view_context_if_not_implemented(self):
        v = ViewContext()
        try:
            v.render()
        except NotImplementedError as e:
            self.assertIsNotNone(e)

    def test_label_order(self):
        labels = {'fn': 'First Name','id': 'Id', 'email': 'Email', 'ln': 'Last Name'}
        ordered = LabelOrder(labels, {'fn': 0, 'ln': 1,  'id': -1 , 'email': -2})
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
