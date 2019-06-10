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



class ManagerSwitchTest():

    def do_something(self, old_manager, new_manager):
        print('old_manager - num items: ' + str(len(old_manager)) + ' structure: ')
        print(old_manager.stuff)

        if new_manager == None:
            print('new_manager - None')
        else:
            print('new_manager - num items: ' + str(len(new_manager)) + ' structure: ')
            print(new_manager.stuff)
        print()


    def manager_switch_test(self):
        """
        Switches back and forth betwee the two managers and checks if the current manager
        has expected number of items
        """
        print('manager_switch_test')

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

        # Test
        for t in range(4):
            if t % 2 == 0:
                manager_switch.switch('manager_1')
                manager = manager_switch.get()

                assert len(manager) == 2, 'manager_1 has an unexpected number of items:  Expected: %s,  Result: %s' % (str(2), str(len(manager)))
                assert 'item_1' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_1"'
                assert 'item_2' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_2"'

            elif t % 2 == 1: 
                manager_switch.switch('manager_2')
                manager = manager_switch.get()

                assert len(manager) == 1, 'manager_2 has an unexpected number of items:  Expected: %s,  Result: %s' % (str(1), str(len(manager)))
                assert 'item_3' in manager.stuff.keys(), 'manager_2 does not contain an item named "item_3"'


    def manager_add_remove_test(self):
        """
        Creates two managers, and removes first one created then second one
        """
        print('manager_add_remove_test')

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
        assert manager_switch.active == 'manager_2', 'manager_2 is not the active manager. Active manager: %s' % (manager_switch.active, )
        assert len(manager) == 1, 'manager_2 has an unexpected number of items:  Expected: %s,  Result: %s' % (str(1), str(len(manager)))
        assert 'item_3' in manager.stuff.keys(), 'manager_2 does not contain an item named "item_3"'

        manager_switch.switch('manager_1')
        manager_switch.rmv('manager_2')
        
        manager = manager_switch.get()
        assert manager_switch.active == 'manager_1', 'manager_1 is not the active manager. Active manager: %s' % (manager_switch.active, )
        assert len(manager) == 2, 'manager_1 has an unexpected number of items:  Expected: %s,  Result: %s' % (str(2), str(len(manager)))
        assert 'item_1' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_1"'
        assert 'item_2' in manager.stuff.keys(), 'manager_1 does not contain an item named "item_2"'

        manager_switch.rmv('manager_1')
        manager = manager_switch.get()

        assert manager == None, 'There still exist a manager'