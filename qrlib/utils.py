import time



def time_it(func):
    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        print('`{}` spend {:.2f}'.format(func.__name__, time.time() - start_time))
    return wrapper



import os
import multiprocessing as mp
from time import sleep


class MultiProcessCommandRunner:
    def __init__(self):
        pass

    def run(self, command_list):
        for command in command_list:
            p = mp.Process(target=self._run_command, args=(command,))
            p.start()
            sleep(5)

    def _run_command(self, command):
        os.system(command)
