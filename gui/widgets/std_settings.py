from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from gui.widgets.editable_value_field import EditableValueField
from osu.local.hitobject.std.std import StdSettings


class StdSettingsGui(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout       = QVBoxLayout()
        self.color_layout = QHBoxLayout()

        self.view_time_back   = EditableValueField(0, 5000, 'View time backward (ms): ')
        self.view_time_ahead  = EditableValueField(0, 5000, 'View time forward (ms): ')
        self.cursor_radius    = EditableValueField(1, 10,   'Cursor radius (px): ')
        self.cursor_thickness = EditableValueField(1, 10,   'Cursor thickness (px): ')
        
        self.color_pick          = QLabel('Picking color for: ')
        self.color_selector      = QColorDialog()
        self.cursor_color_select = QPushButton('Cursor color')

        self.k1_color_select     = QPushButton('K1 color')
        self.k2_color_select     = QPushButton('K2 color')
        self.m1_color_select     = QPushButton('M1 color')
        self.m2_color_select     = QPushButton('M2 color')


    def construct_gui(self):
        self.setLayout(self.layout)

        self.color_layout.addWidget(self.cursor_color_select)
        self.color_layout.addWidget(self.k1_color_select)
        self.color_layout.addWidget(self.k2_color_select)
        self.color_layout.addWidget(self.m1_color_select)
        self.color_layout.addWidget(self.m2_color_select)

        self.layout.addWidget(self.view_time_back)
        self.layout.addWidget(self.view_time_ahead)
        self.layout.addWidget(self.cursor_radius)
        self.layout.addWidget(self.cursor_thickness)
        self.layout.addWidget(self.color_pick)
        self.layout.addLayout(self.color_layout)
        self.layout.addWidget(self.color_selector)

        self.cursor_color_select.clicked.connect(self.__set_cursor_color_select_active)
        self.k1_color_select.clicked.connect(self.__set_k1_color_select_active)
        self.k2_color_select.clicked.connect(self.__set_k2_color_select_active)
        self.m1_color_select.clicked.connect(self.__set_m2_color_select_active)
        self.m2_color_select.clicked.connect(self.__set_m2_color_select_active)

        self.view_time_back.value_changed.connect(StdSettings.set_view_time_back, inst=self.view_time_back)
        self.view_time_ahead.value_changed.connect(StdSettings.set_view_time_ahead, inst=self.view_time_ahead)
        self.cursor_radius.value_changed.connect(StdSettings.set_cursor_radius, inst=self.cursor_radius)
        self.cursor_thickness.value_changed.connect(StdSettings.set_cursor_thickness, inst=self.cursor_thickness)


    def update_gui(self):
        self.view_time_back.set_val(StdSettings.view_time_back)
        self.view_time_ahead.set_val(StdSettings.view_time_ahead)
        self.cursor_radius.set_val(StdSettings.cursor_radius)
        self.cursor_thickness.set_val(StdSettings.cursor_thickness)
        
        self.color_selector.setOptions(QColorDialog.DontUseNativeDialog | QColorDialog.NoButtons | QColorDialog.ShowAlphaChannel)

    
    def __set_cursor_color_select_active(self):
        try: self.color_selector.currentColorChanged.disconnect()
        except TypeError: pass

        self.color_pick.setText('Picking color for: cursor')
        self.color_selector.setCurrentColor(StdSettings.cursor_color)
        self.color_selector.currentColorChanged.connect(StdSettings.set_cursor_color)


    def __set_k1_color_select_active(self):
        try: self.color_selector.currentColorChanged.disconnect()
        except TypeError: pass

        self.color_pick.setText('Picking color for: k1')
        self.color_selector.setCurrentColor(StdSettings.k1_color)
        self.color_selector.currentColorChanged.connect(StdSettings.set_k1_color)


    def __set_k2_color_select_active(self):
        try: self.color_selector.currentColorChanged.disconnect()
        except TypeError: pass

        self.color_pick.setText('Picking color for: k2')
        self.color_selector.setCurrentColor(StdSettings.k2_color)
        self.color_selector.currentColorChanged.connect(StdSettings.set_k2_color)


    def __set_m1_color_select_active(self):
        try: self.color_selector.currentColorChanged.disconnect()
        except TypeError: pass

        self.color_pick.setText('Picking color for: m1')
        self.color_selector.setCurrentColor(StdSettings.m1_color)
        self.color_selector.currentColorChanged.connect(StdSettings.set_m1_color)


    def __set_m2_color_select_active(self):
        try: self.color_selector.currentColorChanged.disconnect()
        except TypeError: pass
            
        self.color_pick.setText('Picking color for: m2')
        self.color_selector.setCurrentColor(StdSettings.m2_color)
        self.color_selector.currentColorChanged.connect(StdSettings.set_m2_color)

    