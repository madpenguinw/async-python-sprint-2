import time

import pytest

from job import Job


def first_task():
    pass


def second_task():
    time.sleep(3)


def third_task():
    raise GeneratorExit()


def fourth_task():
    raise StopIteration()

VARIABLE_FOR_TEST = False

def fifth_task():
    global VARIABLE_FOR_TEST
    if not VARIABLE_FOR_TEST:
        VARIABLE_FOR_TEST = True
        1 / 0
    return None


class TestJob:

    def setup_method(self):
        self.task_1 = Job(
            func=first_task, tries=2, start_at=2, max_working_time=2)
        self.coroutine_1 = self.task_1.run()
        self.task_2 = Job(
            func=second_task, tries=2, start_at=0, max_working_time=2)
        self.coroutine_2 = self.task_2.run()
        self.task_3 = Job(
            func=third_task, tries=2, start_at=0, max_working_time=0)
        self.coroutine_3 = self.task_3.run()
        self.task_4 = Job(
            func=fourth_task, tries=2, start_at=0, max_working_time=0)
        self.coroutine_4 = self.task_4.run()
        self.task_5 = Job(
            func=fifth_task, tries=2, start_at=0, max_working_time=0)
        self.coroutine_5 = self.task_5.run()

    def test_general(self):
        assert self.coroutine_1.send(
            (self.task_1.func, self.task_1.tries, self.task_1.start_at,
                self.task_1.max_working_time)) == None

    def test_time_limit(self):
        assert self.coroutine_2.send(
            (self.task_2.func, self.task_2.tries, self.task_2.start_at,
                self.task_2.max_working_time)) == None

    def test_generator_exit(self):
        with pytest.raises(GeneratorExit):
            self.coroutine_3.send(
                (self.task_3.func, self.task_3.tries, self.task_3.start_at,
                    self.task_3.max_working_time))

    def test_stop_iteration(self):
        with pytest.raises(RuntimeError):
            self.coroutine_4.send(
                (self.task_4.func, self.task_4.tries, self.task_4.start_at,
                    self.task_4.max_working_time))

    def test_exception(self):
        assert self.coroutine_5.send(
            (self.task_5.func, self.task_5.tries, self.task_5.start_at,
                self.task_5.max_working_time)) == None
