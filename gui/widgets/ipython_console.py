import os
import sys
import asyncio

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager



# Thanks https://stackoverflow.com/a/41070191
class IPythonConsole(RichJupyterWidget):
    
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self, customBanner=None, *args, **kwargs):
        super(IPythonConsole, self).__init__(*args, **kwargs)

        if customBanner is not None:
            self.banner = customBanner
        
        # IPython Python 3.8 support fix
        if sys.platform == 'win32' and sys.version_info >= (3, 8):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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

        self.magic('load_ext autoreload')
        self.magic('autoreload 2')

        self.push_vars({ 'exit' : lambda: self.print_text('exit() has been disabled to avoid breaking features') })
        self.push_vars({ 'help' : lambda: self.print_text('help() has been disabled to avoid breaking features') })


    def push_vars(self, variableDict):
        """
        Given a dictionary containing name / value pairs, push those variables
        to the Jupyter console widget
        """
        self.kernel_manager.kernel.shell.push(variableDict)


    def del_var(self, var_name):
        self.kernel_manager.kernel.shell.del_var(var_name)


    def magic(self, command):
        command = command.split(' ')
        self.kernel_manager.kernel.shell.run_line_magic(command[0], ' '.join(command[1:]))


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