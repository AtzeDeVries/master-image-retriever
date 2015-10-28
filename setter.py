#!/usr/bin/env python2.7

from lib import *
import time

mldb = db.connect(config.get('db_host'),
                  config.get('db_user'),
                  config.get('db_password'),
                  config.get('db_name'))

q = mq.redis_connect()

def get_regno_list():
    payload = mq.pop('data:regno_list',q)

    if payload is not None or '':
        files = []
        errors = []
        data = payload
        mq.setex('status:query',q,'running query',300)
        for i in data.split(","):
             query = "SELECT master_file FROM media WHERE regno = '%s'" % i
             mf = db.query(mldb,query)
             if mf:
                 files.append(mf[0]['master_file'])
             else:
                 info = "master file with id: '%s' not found" % i
                 log.logger.warning(info)
                 errors.append(info)

        mq.setex('status:query',q,'done query',300)
        if files:
            files = set(files)
            payload = ",".join(files)
            log.logger.debug(payload)
            mq.put('data:master_list',q,payload)
        if errors:
            mq.put('error:query',q,",".join(errors))


while True:
    mq.setex('status:query',q,'waiting for input')
    get_regno_list()
    time.sleep(1)
