import time
import sched
import pandas
import logging
import requests
from io import StringIO

import utils
from database import upsert_data

DOWNLOAD_URL = "https://data.cdc.gov/api/views/9mfq-cb36/rows.csv?accessType=DOWNLOAD"
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 10         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_csv(url=DOWNLOAD_URL, retries=MAX_DOWNLOAD_ATTEMPT):
    """Downloads the csv file from the web.
    """
    text = None
    for i in range(retries):
        try:
            req = requests.get(url, timeout=30.0)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_csv too many FAILED attempts')
    return text

def filter_csv(text):
    """Converts `text` to `DataFrame`
    """
    df = pandas.read_csv(StringIO(text), usecols=["created_at", "pnew_case", "new_case", "tot_cases", "state"])
    df['date'] = pandas.to_datetime(df['created_at'])
    df.drop(columns=['created_at'], axis=1, inplace=True)
    return df


def update_once():
    csv = download_csv()
    df = filter_csv(csv)
    upsert_data(df)

def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            update_once()
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()
    # txt = download_csv()
    # filter_csv(txt)


