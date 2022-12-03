import time



def time_it(func):
    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        print('`{}` spend {:.2f}'.format(func.__name__, time.time() - start_time))
    return wrapper


class ListGrouper:
    def __init__(self, input_list):
        self._input_list = input_list
        self._length = len(input_list)

    def group_by_step(self, step):
        output_list = []
        for start_idx in range(0, self._length, step):
            end_idx = start_idx + step
            end_idx = end_idx if end_idx < self._length else self._length
            output_list.append(self._input_list[start_idx: end_idx])
        return output_list

    def group_to_several(self, num):
        step = self._length / num + 1
        return self.group_by_step(step)
