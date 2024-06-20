from flask_apscheduler import APScheduler
from external_functionalities.main import web_crawler_main


scheduler = APScheduler()


# 'cron', id='scheduled_task', hour=0


@scheduler.task('cron', id='scheduled_task', hour=0)
def jobs_web_crawler():
  web_crawler_main()
