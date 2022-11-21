from job import Job
from scheduler import Scheduler
from tasks.funcs_for_files import (func_that_sleeps, make_directory,
                                   make_gitignore_file)
from tasks.parser import Parser

if __name__ == '__main__':
    scheduler = Scheduler()
    #  task_1 task may be repeated for 3 times
    task_1 = Job(Parser.start_parser, tries=3)
    task_2 = Job(make_directory)
    # task_3 task should sleep for 2 sec before processing
    task_3 = Job(make_gitignore_file, start_at=2)
    # task_4 task should be terminated
    task_4 = Job(func_that_sleeps, max_working_time=2)
    scheduler.add_task([task_1, task_2, task_3, task_4])
    scheduler.run()
