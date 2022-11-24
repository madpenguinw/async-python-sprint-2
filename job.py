import logging
import time
from multiprocessing import Process
from typing import Callable, Generator

import logger

logger = logging.getLogger(__name__)


def time_limit(func: Callable, time: int) -> None:
    """Runs a function with a time limit"""
    p = Process(target=func)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        logger.info('Task was terminated')
    return


def coroutine(func: Callable) -> Callable:
    def wrap(*args, **kwargs) -> Generator:
        gen = func(*args, **kwargs)
        gen.send(None)
        return gen
    return wrap


class Job:
    def __init__(
        self,
        func: Callable,
        start_at: int = 0,
        max_working_time: int = 0,
        tries: int = 0,
    ):
        self.tries = tries
        self.func = func
        self.start_at = start_at
        self.max_working_time = max_working_time

    @staticmethod
    @coroutine
    def run() -> Generator:
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
            except GeneratorExit and StopIteration:
                logger.info("Job's coroutine is finished")
                raise
            except Exception as error:
                str_error: str = str(error)
                logger.error(str_error)
                attempt = 1
                while tries:
                    logger.error(str_error)
                    logger.error('Attempt № %(attempt)s', {'attempt': attempt})
                    attempt += 1
                    tries -= 1
                    task()
