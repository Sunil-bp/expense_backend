# from celery.decorators import task
# from celery.utils.log import get_task_logger
#
# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
# from django_celery_beat.models import PeriodicTask
#
# logger = get_task_logger(__name__)
#
#
# @periodic_task(run_every=(crontab(seconds='*/10')), name="some_task", ignore_result=True)
# def some_task():
#     print("Printing from celery ")
#
# @task(name="send_feedback_email_task")
# def send_feedback_email_task(email, message):
#     """sends an email when feedback form is filled successfully"""
#     logger.info("Sent feedback email")
#     return "done"


# from celery import shared_task
# @shared_task
# def sum_custom(a,b):
#     print(f"Sum of {a} and {b} is {a+b}")
#     return a+b

import celery
from celery import task

@task()
def elast():
    print("IN elast  ")


