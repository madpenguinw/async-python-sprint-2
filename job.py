import logging
import time
from multiprocessing import Process

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


def time_limit(func, time):
    """Runs a function with a time limit"""
    p = Process(target=func)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        logger.info('Task was terminated')
    return


def coroutine(f):
    def wrap(*args, **kwargs):
        gen = f(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Job:
    def __init__(
        self,
        func,
        start_at=0,
        max_working_time=0,
        tries=0,
    ):
        self.tries = tries
        self.func = func
        self.start_at = start_at
        self.max_working_time = max_working_time

    @coroutine
    def run():
        logger.info("Job's coroutine is running")
        while True:
            try:
                task, tries, start_at, max_working_time = (yield)
                task_name = task.__name__
                logger.info(
                    'Processing task "%(task_name)s"',
                    {'task_name': task_name}
                )
                if start_at:
                    logger.info(
                        'Task starts in %(start_at)s seconds',
                        {'start_at': start_at}
                    )
                    time.sleep(start_at)
                if max_working_time:
                    time_limit(task, max_working_time)
                else:
                    task()
                tries = 0
            except GeneratorExit or StopIteration:
                logger.info("Job's coroutine is finished")
                raise
            except Exception as error:
                print(error)
                attempt = 1
                while tries:
                    logger.error(error)
                    logger.error('Attempt № %(attempt)s', {'attempt': attempt})
                    attempt += 1
                    tries -= 1
                    task()
