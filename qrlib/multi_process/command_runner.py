from .runner import BaseMultiProcessRunner
import os


class CommandRunner(BaseMultiProcessRunner):
    def __init__(self, command_list):
        self._command_list = command_list

    def _item_list(self):
        return self._command_list

    def _process_one_item(self, item):
        command = item
        os.system(command)