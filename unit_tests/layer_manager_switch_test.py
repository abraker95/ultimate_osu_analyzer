import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from core.layer_manager import LayerManager

from gui.widgets.layer_manager_switch import LayerManagerSwitch
from gui.objects.layer.layer import Layer


class LayerManagerSwitchTest(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        
        self.layer_manager_switch = LayerManagerSwitch()
        self.setCentralWidget(self.layer_manager_switch)

        self.layer_manager_switch.add('layer_manager_1', LayerManager())
        self.layer_manager_switch.add('layer_manager_2', LayerManager())
        
        self.layer_manager_switch.switch('layer_manager_1')
        self.layer_manager_switch.get().add_layer('layer_1', Layer('layer_1'))
        self.layer_manager_switch.get().add_layer('layer_2', Layer('layer_2'))

        self.layer_manager_switch.switch('layer_manager_2')
        self.layer_manager_switch.get().add_layer('layer_3', Layer('layer_3'))

        self.layer_manager_switch.switch.connect(self.do_something, inst=self.layer_manager_switch)

        self.setWindowTitle('Layer manager switch test')
        self.show()


    def do_something(self, old_layer_manager, new_layer_manager):
        print('old_layer_manager - num layers: ' + str(len(old_layer_manager)) + ' structure: ')
        print(str(old_layer_manager.get_structure()))
        print('new_layer_manager - num layers: ' + str(len(new_layer_manager)) + ' structure: ')
        print(str(new_layer_manager.get_structure()))
        print()


    def layer_manager_switch_test(self, app):
        print('layer_manager_switch_test')
        for t in range(4):
            if t % 2 == 0:
                self.layer_manager_switch.switch('layer_manager_1')
                layer_manager = self.layer_manager_switch.get()
                structure = layer_manager.get_structure()

                assert len(structure) == 2, 'layer_manager_1 has an unexpected number of layers:  Expected: %s,  Result: %s' % (str(2), str(len(structure)))
                assert 'layer_1' in structure.keys(), 'layer_manager_1 does not contain a layer named "layer_1"'
                assert 'layer_2' in structure.keys(), 'layer_manager_1 does not contain a layer named "layer_2"'

            elif t % 2 == 1: 
                self.layer_manager_switch.switch('layer_manager_2')
                layer_manager = self.layer_manager_switch.get()
                structure = layer_manager.get_structure()

                assert len(structure) == 1, 'layer_manager_2 has an unexpected number of layers:  Expected: %s,  Result: %s' % (str(1), str(len(structure)))
                assert 'layer_3' in structure.keys(), 'layer_manager_2 does not contain a layer named "layer_3"'

            app.processEvents() 
            time.sleep(.1)