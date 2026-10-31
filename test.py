#!/usr/bin/python3

from dotenv import dotenv_values
from hsl3_14582_fully import LogicModule
from hsl3.dummy import Hsl3Framework, Hsl3Slots
import logging
import unittest
import time

config = dotenv_values(".env")


class ModuleTest(unittest.TestCase):
    def setUp(self):
        self.fw = Hsl3Framework("config.json")

        self.input = {"server_name": b"screen1.lan",
                      "port": 2323,
                      "password": config["password"].encode('utf-8'),
                      "ssl": 1,
                      "on": 0,
                      "brightness": 0,
                      "restart_app": 0
                      }

    def create_module(self):
        inputs=Hsl3Slots(self.input)
        store=Hsl3Slots({})
        module = LogicModule(self.fw)
        module.on_init(inputs, store)
        return module

    def test_switchon(self):
        inputs=Hsl3Slots(self.input)
        module = self.create_module()
        inputs["on"].value = 1
        inputs["on"].changed = True
        module.on_calc(inputs)
        self.assertEqual(self.fw.get_output("ok"), True)

    def test_restart_app(self):
        inputs=Hsl3Slots(self.input)
        module = self.create_module()
        inputs["restart_app"].value = 1
        inputs["restart_app"].changed = True
        module.on_calc(inputs)
        self.assertEqual(self.fw.get_output("ok"), True)
        
    
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
