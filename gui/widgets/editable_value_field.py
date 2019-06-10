from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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