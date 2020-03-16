import asyncio
import threading
import time


async def hello():
    print("Running in the loop...")
    flag = 0
    while flag < 10_000:
        with open("T:/test.txt", "a") as f:
            f.write("------")
        flag += 1
    print("Stop the loop")


if __name__ == '__main__':
    coroutine = hello()
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)

    # Pending：未执行状态
    print('1>', task)
    try:
        t1 = threading.Thread(target=loop.run_until_complete, args=(task, ))
        # t1.daemon = True
        t1.start()

        # Running：运行中状态
        time.sleep(1)
        print('2>', task)
        t1.join()
    except KeyboardInterrupt as e:
        # 取消任务
        task.cancel()
        # Cacelled：取消任务
        print('3>', task)
    finally:
        print('4>', task)