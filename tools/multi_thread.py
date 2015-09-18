# coding:utf-8
from multiprocessing import Process, Queue

num_threads = 4


def run_multi_thread(function_list, *args):
    # 将 函数 index, 结果放入队列

    def f(q, chunk):
       for index, func in chunk:
           q.put((index, func(*args)))

    # container for the returned values
    queue = Queue()

    # slice up the list into smaller num_threads lists
    chunks = slice_list(function_list, num_threads)

    # start running in parallel
    procs = [Process(target = f, args = (queue, x) ) for x in chunks]
    for p in procs: p.start()

    # pulling the data out from each process (it will wait until some process calls put)
    # we have to call get as many as as we call put on the Queue.
    func_index_to_func_result_dict = dict([queue.get() for i in range(len(function_list))])

    # merge results into one list (if you want)
    # this is like Reduce function in mapreduce

    result = []
    # 按function_list 的顺序存放结果
    for index, func in enumerate(function_list):
        func_result = func_index_to_func_result_dict[index]
        result.append(func_result)

    return result

# 相同的函数， 不同的参数， args_list :[(1,2),(3,4)]
def run_multi_thread_same_function(same_func, args_list):
    # 将 函数 index, 结果放入队列

    def f(q, chunk):
       for index, args in chunk:
           q.put((index, same_func(*args)))

    # container for the returned values
    queue = Queue()

    # slice up the list into smaller num_threads lists
    chunks = slice_list(args_list, num_threads)

    # start running in parallel
    procs = [Process(target = f, args = (queue, x) ) for x in chunks]
    for p in procs: p.start()

    # pulling the data out from each process (it will wait until some process calls put)
    # we have to call get as many as as we call put on the Queue.
    args_index_to_func_result_dict = dict([queue.get() for i in range(len(args_list))])

    # merge results into one list (if you want)
    # this is like Reduce function in mapreduce

    result = []
    # 按function_list 的顺序存放结果
    for index, Args in enumerate(args_list):
        func_result = args_index_to_func_result_dict[index]
        result.append(func_result)

    return result

def slice_list(li, num_chunks):
    """Slice list into chunks of equal sizes

          slice_list([1,1,2,4] 2) -> [ [(0,1),(1,1)], [(2,2),(3,4)] ]
    """
    start = 0
    result = []
    for i in xrange(num_chunks):
        stop = start + len(li[i::num_chunks])
        result.append(zip(range(start, stop), li[start:stop]))
        start = stop
    return result


if __name__ == "__main__":

    import time
    def A(x, y):
        time.sleep(6)
        return "r_A"

    def B(x, y ):
        time.sleep(6)
        return "r_B"
    def C(x, y ):
        print x, y
        time.sleep(0.1)
        return x + y


    def f_1(*args):
        return C(*args)

    def f_2(args_list):
        for args in args_list:
            C(*args)

    # print f_1(1, 2)
    args_list = [(1,2),(3,4)] * 100
    # f_2(args_list)

    # print slice_list([1,2,3,4], 1)

    print run_multi_thread_same_function_(C, args_list)