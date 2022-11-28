import time



def time_it(func):
    def wrapper(*args, **kw):
        start_time = time.time()
        func(*args, **kw)
        print('`{}` spend {:.2f}'.format(func.__name__, time.time() - start_time))
    return wrapper
