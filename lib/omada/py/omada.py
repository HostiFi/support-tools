import functools

import pymongo

@functools.lru_cache(maxsize=None)
def db():
    return pymongo.MongoClient("mongodb://127.0.0.1:27217").omada

@functools.lru_cache(maxsize=None)
def version():
    version_str = db().systemsetting.find_one()["start_up_info"]["db_version"]
    return tuple(map(int, version_str.split(".")))
