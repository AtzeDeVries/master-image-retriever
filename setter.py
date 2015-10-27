#!/usr/bin/env python2.7

from lib import *
import time
import json

# good restore example:
# directory = /20130610
# file = 1292_HERBARIUMWAG_20130610235917.tar
# restore.getTar('20130718','0235_HERBARIUMWAG_20130718000130.tar')
config.get('db_host')

mldb = db.connect(config.get('db_host'),
                  config.get('db_user'),
                  config.get('db_password'),
                  config.get('db_name'))

mf = db.query(mldb,"SELECT master_file FROM media WHERE regno = '000003338-RMNH.CRUS.D.31690'")
print mf
exit()
#### DOWNLOADING AND INDEXING PART
# requests = restore.getTar(5)
#
# ftp_con = restore.openFTP()
# for req in requests:
#   try:
#     size = restore.checkRemoteFile(ftp_con,req['remote_dir'],req['tar'])
#   except Exception as e:
#     log.logger.debug(e)
#   if size:
#     log.logger.info('Size of ' + req['tar'] + ' : ' + str( round(float(size)/float(1024**2),3) ) + 'MB')
#     #if size > (1*1024*1024):
#       #print 'candidate'
#     try:
#       restore.downloadTar(ftp_con,req['remote_dir'],req['tar'])
#     except Exception as e:
#       log.logger.error(e)
#     try:
#       restore.indexTar(req['tar'])
#     except Exception as e:
#       log.logger.error('Could not index tar')
#
#   else:
#     print 'could not return sizfrom RedisQueue import RedisQueue

#
# restore.closeFTP(ftp_con)
################

##### Extract and convert #############

# try:
#   filename = restore.extractTar(15)
# except Exception as e:
#   log.logger.info(e)
# image.convertToJpeg(filename,'/tmp')

#######################################
#logger = log
#logger.logger.info('ha')
payload = {
    'ids':['a','b','c'],
    'timestamp' : '2014-04-03',
           }

q = mq.redis_connect()
#mq.put('queue:test',q,json.dumps(payload))
while True:
    mq.setex('status:query',q,'running query')
    time.sleep(1)
#master_file = master.get_my_master('000003366-000003338-RMNH.CRUS.D.31690')
#master.copy_my_master(master_file,'/tmp')

#### use this to update ml_wag database with good filename search
# match.updateFilename()
####



###### Image Matching ################
# print image.matchHistogram('/tmp/000704693-WAG.1512446.jpg','/tmp/000704682-WAG.1392547.jpg')
# print image.matchHistogram('/tmp/000704693-WAG.1512446.jpg','/tmp/000704693-WAG.1512446.jpg')
############################# #########
