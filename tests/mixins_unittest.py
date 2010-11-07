""" Protocol tests """

import unittest
from json import JSONEncoder, JSONDecoder
from tests import common

from pynpoint.mixins import Mixin
from pynpoint.protocol.handlers import announcement, export, query

class MixinTestCase(unittest.TestCase):
    def setUp(self):
        self.expected_mixins = [announcement.Announcement,
                                export.Export,
                                query.Query,
                                None]

    def test_get_mixin(self):
        keys = 'hi!', 'i have', 'heard of?', None

        actual_mixins = [Mixin.get_mixin(key) for key in keys]

        for ex, ac in zip(self.expected_mixins, actual_mixins):
            self.assertEqual(ex, ac)

    def test_that_mixins_work(self):
        class A(object):
            pass

        class B(A):
            pass

        for mixin in self.expected_mixins: 
            if mixin:
                with Mixin(A(), mixin) as mixed:
                    self.assertTrue(mixin in mixed.__class__.__bases__)
                    self.assertFalse(mixin in B.__bases__)

                self.assertFalse(mixin in mixed.__class__.__bases__)
                self.assertFalse(mixin in B.__bases__)
            else:
                self.assertRaises(TypeError, Mixin, (A(), mixin))


    def test_underunder_enter_and_underunder_exit(self):
        class A(object):
            pass

        class B(A):
            pass

        for mixin in self.expected_mixins:
            if mixin:
                mixee = Mixin(A(), mixin)
                mixee.__enter__()
                self.assertTrue(mixin in A.__bases__)
                self.assertFalse(mixin in B.__bases__)
                mixee.__exit__()
                self.assertFalse(mixin in A.__bases__)
                self.assertFalse(mixin in B.__bases__)


    def test_registration(self):
        class TestMixin:
            pass

        self.assertTrue(Mixin.register('mixin', TestMixin))
        self.assertTrue(Mixin.unregister('mixin'))
        self.assertFalse(Mixin.unregister('mixin'))
