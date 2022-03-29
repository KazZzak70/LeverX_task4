from django.core.management.base import BaseCommand
from reports.tasks import LowPriorityTask, HighPriorityTask


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("calling_mode", type=str)

    def handle(self, *args, **options):
        if options["calling_mode"] == "1":
            for n in range(5):
                LowPriorityTask().apply_async(kwargs={"task_number": n}, serializer="json", queue='lowpriorityqueue')
        elif options["calling_mode"] == "2":
            for n in range(5):
                HighPriorityTask().apply_async(kwargs={"task_number": n}, serializer="json", queue='highpriorityqueue')
        elif options["calling_mode"] == "3":
            for n in range(2):
                LowPriorityTask().apply_async(kwargs={"task_number": n},
                                              priority=9,
                                              serializer="json",
                                              queue='lowpriorityqueue')
                HighPriorityTask().apply_async(kwargs={"task_number": n},
                                               priority=0,
                                               serializer="json",
                                               queue='highpriorityqueue')
