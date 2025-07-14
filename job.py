from apscheduler.schedulers.blocking import BlockingScheduler

from tips import tips


def job():
    tips()


scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', hour='0/4')  # 从0点开始每4小时执行
scheduler.start()
