import time
import redis
import asyncio
from queue import Queue
from threading import Thread
from zredis import redis_connect


def start_loop(loop):
    # 一个在后台永远运行的事件循环
    asyncio.set_event_loop(loop)
    loop.run_forever()


# async def do_sleep(x, queue):
#     print(f'do_sleep({x})')
#     await asyncio.sleep(x)
#     queue.put(f"do_sleep({x}): ok")


async def do(task):
    log_queue.put(f'task:{task} begin')
    asyncio.sleep(1.5)
    log_queue.put(f'task:{task} end')


def consumer():
    while True:
        task = redis.brpop("queue")
        print(f'task:{task}')
        job = asyncio.wait_for(do, timeout=2)
        asyncio.run_coroutine_threadsafe(job, new_loop)
        # job = asyncio.wait_for(do_sleep(int(task), log_queue), timeout=2)
        # asyncio.run_coroutine_threadsafe(job, new_loop)


if __name__ == '__main__':
    print(time.ctime())
    new_loop = asyncio.new_event_loop()

    # 定义一个线程，运行一个事件循环对象，用于实时接收新任务
    loop_thread = Thread(target=start_loop, args=(new_loop, ))
    loop_thread.setDaemon(True)
    loop_thread.start()
    # 创建redis连接
    redis = redis_connect()

    log_queue = Queue()

    # 子线程：用于消费队列消息，并实时往事件对象容器中添加新任务
    consumer_thread = Thread(target=consumer)
    consumer_thread.setDaemon(True)
    consumer_thread.start()

    while True:
        msg = log_queue.get()
        print(f"协程运行完: {msg}")
        print("当前时间：", time.time())