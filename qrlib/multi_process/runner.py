import multiprocessing as mp
from abc import ABC, abstractmethod
from tqdm import tqdm


class BaseMultiProcessRunner(ABC):
    """
    多进程的抽象类
    """
    @abstractmethod
    def __init__(self):
        """
        需要实现的抽象方法
        """
        pass

    @abstractmethod
    def _item_list(self):
        """
        需要实现的抽象方法
        """
        pass

    @abstractmethod
    def _process_one_item(self, item):
        """
        需要实现的抽象方法
        """
        pass

    def _item_queue(self):
        manager = mp.Manager()
        item_queue = manager.Queue()

        for item in self._item_list():
            item_queue.put(item)

        return item_queue

    def _before_loop_when_single_process(self):
        pass

    def _after_loop_when_single_process(self):
        pass

    def _before_loop_when_multi_process(self):
        pass

    def _after_loop_when_multi_process(self):
        pass

    def single_process(self, show_progress=True):
        self._before_loop_when_single_process()
        for item in (tqdm(self._item_list()) if show_progress else self._item_list()):
            self._process_one_item(item)
        self._after_loop_when_single_process()

    def multi_process(self, num_process, show_progress=True):
        item_queue = self._item_queue()

        pool = mp.Pool()
        for _ in range(num_process):
            # todo: how to save result_total
            pool.apply_async(self._run_when_multi_process, args=(item_queue, show_progress))

        pool.close()
        pool.join()

    def _run_when_multi_process(self, item_queue, show_progress):
        self._before_loop_when_multi_process()
        while True:
            try:
                item = item_queue.get(False)
            except:
                print('Item queue is empty.')
                break
            else:
                self._process_one_item(item)
                if show_progress:
                    print('There are still {} items which need to process.'.format(item_queue.qsize()))
        self._after_loop_when_multi_process()