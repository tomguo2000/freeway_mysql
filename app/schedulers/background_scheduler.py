from apscheduler.schedulers.background import BackgroundScheduler

import config

from app.schedulers.job_schedule_test import job_schedule_test
from app.schedulers.job_ranger import job_ranger_main
# from app.schedulers.delete_unverified_users_cron_job import delete_unverified_users_job

scheduler = BackgroundScheduler()


def init_schedulers():
    """Init all schedulers"""
    # remove all jobs before init
    scheduler.remove_all_jobs()

    # add a scheduler here
    init_ranger_scheduler()
    init_test_scheduler()

    if not scheduler.running:
        scheduler.start()


def init_ranger_scheduler():
    scheduler.add_job(
        id="job_ranger",
        func=job_ranger_main,
        trigger="interval",
        seconds=2000,
        timezone="Asia/Shanghai",
        # replace_existing=True,
    )

def init_test_scheduler():
    scheduler.add_job(
        id="job_schedule_test",
        func=job_schedule_test,
        trigger="date",
        run_date="2022-03-07 17:36:00",
        timezone="Asia/Shanghai",
        # replace_existing=True,
    )
