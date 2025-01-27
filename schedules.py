import schedule
import time
from db import DataBase
import logging

db = DataBase()


def schedules():
    schedule.every().day.at("03:00", "Asia/Omsk").do(db.close_duty)
    print("Scheduled")
    while True:
        schedule.run_pending()
        time.sleep(1)

