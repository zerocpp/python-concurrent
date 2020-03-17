'''
异步框架
'''
import asyncio
from queue import Queue
from threading import Thread
import random
import time
import traceback
import requests
import aiohttp


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


main_loop = asyncio.get_event_loop()

task_loop = asyncio.new_event_loop()
task_thread = Thread(target=start_loop, args=(task_loop, ))
task_thread.setDaemon(True)
task_thread.start()


async def fetch(proxy):
    async with aiohttp.ClientSession(timeout=30) as session:
        url = 'http://127.0.0.1:9999/visit'
        for _ in range(10):
            async with session.get(url) as resp:
                print(await resp.text())


def get_proxy():
    return random.randint(1, 1000)


def main():
    begin_time = time.time()
    proxy = get_proxy()
    print(f'代理: {proxy}')

    while True:
        time.sleep(1)
        if time.time() - begin_time > 30:
            proxy = get_proxy()
            begin_time = time.time()
            print(f'更换代理: {proxy}')
            asyncio.gather
        asyncio.run_coroutine_threadsafe(asyncio.wait(fetch(proxy), timeout=5),
                                         task_loop)
        # task_loop.run_until_complete(consumer(proxy))


if __name__ == "__main__":
    main()

# async def main(loop):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for i in range(2):
#             task = asyncio.create_task(do_task(session, f"task{i}"))
#             tasks.append(task)
#         # tasks = [task_loop.create_task(do_task(session, f"task({i})")) for i in range(1_000)]
#         gather_task = asyncio.wait(tasks, timeout=2)
#         # loop.run_until_complete(gather_task)
#         asyncio.run_coroutine_threadsafe(gather_task, loop)

# main_loop = asyncio.get_event_loop()
# main_loop.run_until_complete(main(task_loop))

# # # loop = asyncio.get_event_loop()
# # # tasks = [asyncio.ensure_future(do_task(i)) for i in range(1, 11)]
# # tasks = [do_task(i) for i in range(1, 11)]
# # # tasks = [asyncio.wait_for(do_task(i), timeout=2) for i in range(1, 11)]
# # try:
# #     # dones, pendings = loop.run_until_complete(asyncio.gather(*tasks))
# #     dones, pendings = task_loop.run_until_complete(
# #         asyncio.wait(tasks, timeout=2))
# #     print(len(dones), len(pendings))
# #     for t in pendings:
# #         t.cancel()
# # except asyncio.TimeoutError as ex:
# #     print(f'timeout: {ex}')
# #     traceback.print_exc()
# # except Exception as ex:
# #     print(f'ex: {ex}')
# #     traceback.print_exc()

# # while True:
# #     time.sleep(1)
# # finally:
# #     task_loop.close()

# # try:
# #     dones, pendings = loop.run_until_complete(
# #         asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
# #     print(len(dones), len(pendings))
# #     dones2, pendings2 = loop.run_until_complete(
# #         asyncio.wait(pendings, timeout=2))
# #     print(len(dones2), len(pendings2))
# #     dones3, pendings3 = loop.run_until_complete(asyncio.wait(pendings2))
# #     print(len(dones3), len(pendings3))
# # except Exception as ex:
# #     print(f'ex: {ex}')
