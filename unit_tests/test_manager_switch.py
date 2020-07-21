import unittest
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.manager_switch import ManagerSwitch
from gui.objects.layer.layer import Layer


class Item():

    def __init__(self, key):
        self.key = key


class DummyManager(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.stuff = {}


    def __len__(self):
        return len(self.stuff)

    
    def add_item(self, item):
        self.stuff[item.key] = item


    def rmv_thing(self, key):
        if key in self.stuff: del self.stuff[key]



class TestManagerSwitch(unittest.TestCase):

    def do_something(self, old_manager, new_manager):
        print('old_manager - num items: ' + str(len(old_manager)) + ' structure: ')
        print(old_manager.stuff)

        if new_manager == None:
            print('new_manager - None')
        else:
            print('new_manager - num items: ' + str(len(new_manager)) + ' structure: ')
            print(new_manager.stuff)
        print()


    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])


    def test_manager_switch(self):
        """
        test_manager_switch

        Switches back and forth between the two managers and checks if the current manager
        has expected number of items
        """
        # Setup
        manager_switch = ManagerSwitch()

        manager_switch.add('manager_1', DummyManager())        
        manager_switch.switch('manager_1')
        manager_switch.get().add_item(Item('item_1'))
        manager_switch.get().add_item(Item('item_2'))

        manager_switch.add('manager_2', DummyManager())
        manager_switch.switch('manager_2')
        manager_switch.get().add_item(Item('item_3'))

        manager_switch.switch.connect(self.do_something, inst=manager_switch)

        for t in range(4):
            # Even vals
            if t % 2 == 0:
                manager_switch.switch('manager_1')
                manager = manager_switch.get()

                self.assertEqual(len(manager), 2, 'manager_1 has an unexpected number of items')
                self.assertTrue('item_1' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_1"')
                self.assertTrue('item_2' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_2"')

            # Odd vals
            elif t % 2 == 1: 
                manager_switch.switch('manager_2')
                manager = manager_switch.get()

                self.assertEqual(len(manager), 1, 'manager_2 has an unexpected number of items')
                self.assertTrue('item_3' in manager.stuff.keys(), 'manager_2 does not contain an item named "item_3"')


    def test_manager_add_remove(self):
        """
        test_manager_add_remove

        Creates two managers, removes first one created, and then second one
        """
        # Setup
        manager_switch = ManagerSwitch()

        manager_switch.add('manager_1', DummyManager())        
        manager_switch.switch('manager_1')
        manager_switch.get().add_item(Item('item_1'))
        manager_switch.get().add_item(Item('item_2'))

        manager_switch.add('manager_2', DummyManager())
        manager_switch.switch('manager_2')
        manager_switch.get().add_item(Item('item_3'))

        manager_switch.switch.connect(self.do_something, inst=manager_switch)

        manager = manager_switch.get()
        self.assertEqual(manager_switch.active, 'manager_2', f'manager_2 is not the active manager. Active manager: {(manager_switch.active, )}')
        self.assertEqual(len(manager), 1, 'manager_2 has an unexpected number of items')
        self.assertTrue('item_3' in manager.stuff.keys(), 'manager_2 does not contain an item named "item_3"')

        manager_switch.switch('manager_1')
        manager_switch.rmv('manager_2')
        
        manager = manager_switch.get()
        self.assertEqual(manager_switch.active, 'manager_1', f'manager_1 is not the active manager. Active manager: {(manager_switch.active, )}')
        self.assertEqual(len(manager), 2, 'manager_1 has an unexpected number of items')
        self.assertTrue('item_1' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_1"')
        self.assertTrue('item_2' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_2"')

        manager_switch.rmv('manager_1')
        manager = manager_switch.get()

        self.assertIsNone(manager, 'There still exists a manager')