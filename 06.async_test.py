import time
import redis
import asyncio
from queue import Queue
from threading import Thread


def start_loop(loop):
    # 一个在后台永远运行的事件循环
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def do_sleep(x, queue):
    print(f'do_sleep({x})')
    await asyncio.sleep(x)
    queue.put(f"do_sleep({x}): ok")


def get_redis():
    connection_pool = redis.ConnectionPool(host='172.16.6.115',
                                           port=30379,
                                           db=5)
    return redis.Redis(connection_pool=connection_pool)


def consumer():
    while True:
        _, task = rcon.brpop("queue")
        if not task:
            time.sleep(1)
            continue
        job = asyncio.wait_for(do_sleep(int(task), queue), timeout=2)
        asyncio.run_coroutine_threadsafe(job, new_loop)


async def do_task():
    while True:
        _, task = rcon.brpop("queue")
        job = asyncio.wait_for()


if __name__ == '__main__':
    print(time.ctime())
    new_loop = asyncio.new_event_loop()

    # 定义一个线程，运行一个事件循环对象，用于实时接收新任务
    loop_thread = Thread(target=start_loop, args=(new_loop, ))
    loop_thread.setDaemon(True)
    loop_thread.start()
    # 创建redis连接
    rcon = get_redis()

    queue = Queue()

    # 子线程：用于消费队列消息，并实时往事件对象容器中添加新任务
    consumer_thread = Thread(target=consumer)
    consumer_thread.setDaemon(True)
    consumer_thread.start()

    while True:
        msg = queue.get()
        print(f"协程运行完: {msg}")
        print("当前时间：", time.time())