import logging
import time
from django_courses.celery import app


logging.basicConfig(level=logging.NOTSET)


class LowPriorityTask(app.Task):
    name = "lowprioritytask"

    def run(self, task_number: int):
        logging.info(msg=f"Low priority task number {task_number} called")
        time.sleep(5)
        logging.info(msg=f"Low priority task number {task_number} finished")


class HighPriorityTask(app.Task):
    name = "highprioritytask"

    def run(self, task_number: int):
        logging.info(msg=f"High priority task number {task_number} called")
        time.sleep(15)
        logging.info(msg=f"High priority task number {task_number} finished")


app.register_task(HighPriorityTask)
app.register_task(LowPriorityTask)
