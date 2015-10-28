#!/usr/bin/env python2.7

from lib import *
import time
import os, shutil
import datetime
import zipfile

q = mq.redis_connect()

def get_master_list():

    cwd = os.path.dirname(os.path.realpath("__file__"))
    os.chdir(cwd)
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    if not os.path.exists('tmp/master_files'):
        os.makedirs('tmp/master_files')

    payload = mq.pop('data:master_list',q)
    if payload is not None or '':
        #files = []
        data = payload
        mq.setex('status:master_file',q,'getting master files',300)
        timestamp = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
        newdir = "tmp/master_files/%s/" %  timestamp
        zf = zipfile.ZipFile(os.path.join('./tmp/master_files',timestamp+".zip"),mode='w')
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        for i in data.split(","):
            os.chdir(cwd)
            newname = os.path.join(newdir,i.split("/")[-1][10:])
            shutil.copy2(i,newname)
            print i
            print newname
            os.chdir(newdir)
            zf.write(i.split("/")[-1][10:])

        zf.close()
        os.chdir(os.path.join(cwd,'tmp/master_files'))
        shutil.rmtree(timestamp)
        mq.setex('status:master_file',q,'done getting master files',5)
        ziploc = os.path.join('tmp/master_files',timestamp+".zip")
        log.logger.debug("created zipfile at: %s" % ziploc)
        if mq.exists('data:zip',q):
            mq.delete('data:zip',q)
        mq.put('data:zip',q,ziploc)
        os.chdir(cwd)

while True:
    mq.setex('status:master_file',q,'waiting for input')
    get_master_list()
    time.sleep(1)
