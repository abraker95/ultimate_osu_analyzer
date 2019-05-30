from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from osu.local.hitobject.mania.mania import ManiaSettings
from misc.callback import callback


class EditableValueField(QWidget):

    def __init__(self, min_val, max_val, name):
        QWidget.__init__(self)

        self.layout = QHBoxLayout()
        self.label  = QLabel(name)
        self.text   = QLineEdit()
        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.slider)

        self.label.setFixedWidth(130)
        self.text.setFixedWidth(35)
        self.setFixedHeight(50)

        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)

        self.text.returnPressed.connect(self.__text_value_changed)
        self.slider.valueChanged.connect(self.__slider_value_changed)


    def set_val(self, val):
        self.slider.setValue(val)


    def __text_value_changed(self):
        val = float(self.text.text())
        if val < self.slider.minimum(): self.text.setText(str(self.slider.minimum()))
        if val > self.slider.maximum(): self.text.setText(str(self.slider.maximum()))
        
        self.slider.blockSignals(True)
        self.slider.setValue(val)
        self.slider.blockSignals(False)

        self.value_changed(val)


    def __slider_value_changed(self, val):
        self.text.blockSignals(True)
        self.text.setText(str(val))
        self.text.blockSignals(False)

        self.value_changed(val)


    @callback
    def value_changed(self, val):
        self.value_changed.emit(val, inst=self)



class ManiaSettingsGui(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.init_gui_elements()
        self.construct_gui()
        self.update_gui()


    def init_gui_elements(self):
        self.layout = QVBoxLayout()

        self.viewable_time_interval = EditableValueField(100, 10000, 'Viewable time interval (ms): ')
        self.note_width             = EditableValueField(10, 127,    'Note width (px): ')
        self.note_height            = EditableValueField(1, 50,      'Note height (ms): ')
        self.note_seperation        = EditableValueField(0, 100,     'Note seperation (px): ')
        self.replay_opacity         = EditableValueField(0, 50,      'Replay opacity (%): ')


    def construct_gui(self):
        self.setLayout(self.layout)

        self.layout.addWidget(self.viewable_time_interval)
        self.layout.addWidget(self.note_width)
        self.layout.addWidget(self.note_height)
        self.layout.addWidget(self.note_seperation)
        self.layout.addWidget(self.replay_opacity)

        self.viewable_time_interval.value_changed.connect(ManiaSettings.set_viewable_time_interval, inst=self.viewable_time_interval)
        self.note_width.value_changed.connect(ManiaSettings.set_note_width, inst=self.note_width)
        self.note_height.value_changed.connect(ManiaSettings.set_note_height, inst=self.note_height)
        self.note_seperation.value_changed.connect(ManiaSettings.set_note_seperation, inst=self.note_seperation)
        self.replay_opacity.value_changed.connect(ManiaSettings.set_replay_opacity, inst=self.replay_opacity)


    def update_gui(self):
        self.viewable_time_interval.set_val(ManiaSettings.viewable_time_interval)
        self.note_width.set_val(ManiaSettings.note_width)
        self.note_height.set_val(ManiaSettings.note_height)
        self.note_seperation.set_val(ManiaSettings.note_seperation)
        self.replay_opacity.set_val(ManiaSettings.replay_opacity)