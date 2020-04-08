import time

from zsysargs import get_all_params
__time_prefix = ''
try:
    if int(get_all_params(log_enabled=False).get('LOCAL', '0')):
        __time_prefix = __get_now_iso_0800()
except Exception as ex:
    pass


def __get_now_iso_0800():
    import pytz
    import datetime
    import time
    return datetime.datetime.fromtimestamp(int(
        time.time()), pytz.timezone('Asia/Shanghai')).isoformat()


def log(*values):
    print(__time_prefix, *values, flush=True)


def format_seconds(seconds):
    seconds = int(seconds)
    return "%d:%02d:%02d" % (seconds // 3600, seconds % 3600 // 60,
                             seconds % 60)


class TaskRecorder:
    """任务计时器"""

    def __init__(self, task_name=None, total_count=1, partition_count=1):
        self.task_name = task_name
        if not self.task_name:
            self.task_name = '任务'
        self.total_count = total_count
        self.partition_count = partition_count
        self.begin_at = time.time()

    def get_begin_time(self):
        if not self.begin_at:
            self.begin_task()
        return self.begin_at

    def begin_task(self, log_enabled=True):
        self.begin_at = time.time()
        if log_enabled:
            log(f"【{self.task_name}】开始")

    def end_task(self):
        self.end_at = time.time()

    def log_task(self, msg=None):
        log_msg = f", {msg}" if msg else ""
        log(f"【{self.task_name}】完成, 耗时{format_seconds(self.end_at - self.get_begin_time())}{log_msg}."
            )

    def log_finished(self, msg=None):
        self.end_task()
        self.log_task(msg=msg)

    def log_before(self, index):
        if index == 0:
            return
        finish_part = index
        if finish_part % (self.total_count // self.partition_count) == 0:
            remain_part = (self.total_count - finish_part)
            now = time.time()
            begin = self.get_begin_time()
            cost = now - begin
            remain_seconds = cost / finish_part * remain_part
            remain_seconds_msg = f", 剩余时间: {format_seconds(remain_seconds)}"
            log(f"【{self.task_name}】进度: {finish_part}/{self.total_count}{remain_seconds_msg}"
                )

    def log_after(self, index):
        finish_part = index + 1
        if finish_part % (self.total_count // self.partition_count) == 0:
            remain_part = (self.total_count - finish_part)
            now = time.time()
            begin = self.get_begin_time()
            cost = now - begin
            remain_seconds = cost / finish_part * remain_part
            remain_seconds_msg = f", 剩余时间: {format_seconds(remain_seconds)}"
            log(f"【{self.task_name}】进度: {finish_part}/{self.total_count}{remain_seconds_msg}"
                )


def main():
    log('123')


if __name__ == '__main__':
    main()
