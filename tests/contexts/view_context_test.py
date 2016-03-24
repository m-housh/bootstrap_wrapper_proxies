from unittest import TestCase

from proxies import BaseViewContext, ViewContext
from bootstrap_wrapper import Table, Div

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


    def test_tag_sets_to_class_if_instance_passed_in(self):
        class Test(ViewContext):
            tag = Table()
        
        t = Test()
        self.assertEqual(t.tag, Table)


    def test_tag_kwargs_on_render(self):
        v = ViewContext()
        mv = v.render(tag_kwargs={'style': 'somestyle'})
        tv = Div(style='somestyle').render()
        self.assertEqual(mv, tv)

        mv = v.render()
        tv = Div().render()
        self.assertEqual(mv, tv)
