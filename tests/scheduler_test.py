from scheduler import Scheduler
from job import Job


def first_job():
    pass


def second_job():
    pass


def third_job():
    pass


class TestScheduler:

    def setup_method(self):
        self.scheduler = Scheduler()
        self.custom_scheduler = Scheduler(pool_size=15)
        self.task_1 = Job(first_job, tries=3)
        self.task_2 = Job(second_job, max_working_time=2)
        self.task_3 = Job(third_job, start_at=2)

    def test_queue_before_run(self):
        self.scheduler.add_task([self.task_1, self.task_2, self.task_3])
        assert len(self.scheduler.queue) == 3

    def test_queue_after_run(self):
        self.scheduler.add_task([self.task_1, self.task_2, self.task_3])
        self.scheduler.run()
        assert len(self.scheduler.queue) == 0

    def test_pool_size(self):
        self.scheduler.add_task(
            [
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
            ]
        )
        assert len(self.scheduler.queue) == 10

    def test_custom_scheduler_pool_size(self):
        self.custom_scheduler.add_task(
            [
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
                self.task_1, self.task_2, self.task_3,
            ]
        )
        assert len(self.custom_scheduler.queue) == 15

    def test_get_task_before_run(self):
        self.scheduler.add_task([self.task_1, self.task_2, self.task_3])
        assert self.scheduler.get_task() == self.task_1

    def test_get_task_after_run(self):
        self.scheduler.add_task([self.task_1, self.task_2, self.task_3])
        self.scheduler.run()
        assert self.scheduler.get_task() == None

    def test_run(self):
        self.scheduler.add_task([self.task_1])
        assert self.scheduler.run() == None

    def test_break(self):
        self.scheduler.add_task([None])
        assert self.scheduler.run() == None
