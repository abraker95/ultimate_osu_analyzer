import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from qtconsole.qt import QtGui
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager



# Thanks https://stackoverflow.com/a/41070191
class IPythonConsole(RichJupyterWidget):
    
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self, customBanner=None, *args, **kwargs):
        super(IPythonConsole, self).__init__(*args, **kwargs)

        if customBanner is not None:
            self.banner = customBanner
        
        self.font_size = 6
        self.kernel_manager = QtInProcessKernelManager()

        self.kernel_manager.start_kernel(show_banner=False)
        self.kernel_manager.kernel.gui = 'qt'
        
        self.kernel_client = self.kernel_manager.client()
        self.kernel_client.start_channels()

        def stop():
            self.kernel_client.stop_channels()
            self.kernel_manager.shutdown_kernel()        
        
        self.exit_requested.connect(stop)


    def push_vars(self, variableDict):
        """
        Given a dictionary containing name / value pairs, push those variables
        to the Jupyter console widget
        """
        self.kernel_manager.kernel.shell.push(variableDict)


    def clear(self):
        """
        Clears the terminal
        """
        self._control.clear()


    def print_text(self, text):
        """
        Prints some plain text to the console
        """
        self._append_plain_text(text)


    def execute_command(self, command):
        """
        Execute a command in the frame of the console widget
        """
        self._execute(command, False)