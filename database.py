import logging
import pymongo
import pandas as pds
import expiringdict

import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')
RESULT_CACHE_EXPIRATION = 10             # seconds


def upsert_data(df):
    """
    Update MongoDB database `corona` and regional collections with the given `DataFrame`.
    """
    db = client.get_database("corona")
    update_count = 0
    for record in df.to_dict('records'):
        collection = db.get_collection(record['state'].lower())
        result = collection.replace_one(
            filter={'date': record['date']},            # locate the document if exists
            replacement=record,                         # latest document
            upsert=True)                                # update if exists, insert if not
        if result.matched_count > 0:
            update_count += 1

    logger.info(f"rows={df.shape[0]}, update={update_count}, "
          f"insert={df.shape[0]-update_count}")

def fetch_all_data(state):
    db = client.get_database("corona")
    collection = db.get_collection(state)
    ret = list(collection.find())
    logger.info(str(len(ret)) + ' documents read from the db')
    return ret

_fetch_all_data_as_df_cache = expiringdict.ExpiringDict(max_len=1,
                                                       max_age_seconds=RESULT_CACHE_EXPIRATION)


def fetch_all_data_as_df(state, allow_cached=False):
    """Converts list of dicts returned by `fetch_all_data` to DataFrame with ID removed
    Actual job is done in `_worker`. When `allow_cached`, attempt to retrieve timed cached from
    `_fetch_all_data_as_df_cache`; ignore cache and call `_work` if cache expires or `allow_cached`
    is False.
    """
    def _work():
        data = fetch_all_data(state)
        if len(data) == 0:
            return None
        df = pds.DataFrame.from_records(data)
        df.drop('_id', axis=1, inplace=True)
        return df

    if allow_cached:
        try:
            return _fetch_all_data_as_df_cache['cache']
        except KeyError:
            pass
    ret = _work()
    _fetch_all_data_as_df_cache['cache'] = ret
    return ret


if __name__ == '__main__':
    print(fetch_all_data_as_df('ri'))
