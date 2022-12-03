import argparse  # 1、导入argpase包
import sys


class CommandArgument:
    def __init__(self, description=''):
        self._argument_parser = argparse.ArgumentParser(description=description)
        self._is_parsed = False

    def add(self, name, **kwargs):
        # name, type, default, help
        self._argument_parser.add_argument(f'--{name}', **kwargs)

    def set(self, name_value_dict):
        name_value_list = []
        for name, value in name_value_dict.items():
            name_value_list.append(f'--{name}')
            name_value_list.append(str(value))
        sys.argv.extend(name_value_list)

    def _parse_args(self):
        self._args = self._argument_parser.parse_args()
        self._is_parsed = True

    def __getattr__(self, opt_name):
        if self._is_parsed is not True:
            self._parse_args()
        return getattr(self._args, opt_name)