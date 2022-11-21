import logging

from job import Job

FORMAT = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
DATEFMT = '%Y-%m-%dT%H:%M:%S'

logging.basicConfig(
    format=FORMAT,
    datefmt=DATEFMT,
    level=logging.INFO,
)

formatter = logging.Formatter(
    FORMAT,
    datefmt=DATEFMT
)


logger = logging.getLogger(__name__)


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Scheduler:
    def __init__(self, pool_size: int = 10):
        self.queue = []
        self.tasks_dict = {}
        self.pool_size = pool_size
        self.job_to_do = Job.run()

    def add_task(self, tasks: list):
        length = len(tasks)
        logger.info('Tasks gotten: %(length)s', {'length': length})
        if length > self.pool_size:
            for task in tasks[:self.pool_size]:
                self.queue.append(task)
        else:
            for task in tasks:
                self.queue.append(task)

    def get_task(self):
        if not self.queue:
            logger.info('Empty queue')
            return False
        else:
            task = self.queue.pop(0)
            logger.info('Got task from queue')
            return task

    def run(self):
        task = True
        while task:
            task = self.get_task()
            if task:
                self.job_to_do.send((
                    task.func,
                    task.tries,
                    task.start_at,
                    task.max_working_time,
                ))
