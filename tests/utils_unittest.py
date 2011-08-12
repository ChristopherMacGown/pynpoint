import os
import unittest

from pynpoint import exc
from pynpoint import utils


class UtilsTestCase(unittest.TestCase):
    def test_successful_execute(self):
        exp = [f[2] for f in os.walk("tests/data")][0]

        self.assertEqual(exp, str.split(utils.execute("ls", "tests/data")))

    def test_unsuccessful_execute(self):
        cmd = ("ls", "/foo",)
        self.assertRaises(exc.ExecutionError, utils.execute, *cmd)

        exp = exc.ExecutionError(stderr='ls: /foo: No such file or directory\n',
                                 stdout='',
                                 return_code=1,
                                 cmd=str.join(" ", cmd))
        
        try:
            utils.execute(*cmd)
        except exc.ExecutionError, e:
            self.assertEqual(str(e), str(exp))

    def test_successful_object_load(self):
        self.assertEqual(os, utils.import_object("os"))

        load = utils.import_object("pynpoint.exc.ProtocolError")
        self.assertEqual(exc.ProtocolError().__class__, load.__class__)


    def test_unsuccessful_object_load(self):
        self.assertRaises(exc.ClassNotFound,
                          utils.import_object,
                          "fake_object_that_totally_doesnt_exist")

        self.assertRaises(exc.ClassNotFound,
                          utils.import_object,
                          "a.module_chain.with.a.class.that.doesnt.exist")

        # try to dynamically load a class that doesn't exist in a builtin
        self.assertRaises(exc.ClassNotFound, 
                          utils.import_object, "os.ThisClassDoesntExist")

