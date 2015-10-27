#import config
#import log
import sys
from . import db
from . import config
from . import log
from datetime import datetime
#import db
import shutil
import os

def get_my_master(image_id):
    try:
        ml_db = db.connect(config.get('db_host'),config.get('db_user'),config.get('db_password'),config.get('db_name'))
        log.logger.info('Succesfully connected to database on: ' + config.get('db_name') + '@' + config.get('db_host'))
    except Exception as e:
        log.logger.critical('Could not connect database to :' + config.get('db_name') + '@' + config.get('db_host'))
        log.logger.critical(e)
        exit(1)

    q = 'SELECT master_file FROM media WHERE regno = "' + image_id + '"'
    master_file = None
    try:
        master_file = db.query(ml_db,q)
        log.logger.debug('Succesfully queried tha ml database')
    except Exception as e:
        log.logger.critical('Unable to query ml database with ' + q)
        log.logger.critical(e)
        exit(1)

    log.logger.info('Found master file at' + master_file[0]['master_file'])
    return(master_file[0]['master_file'])

def copy_my_master(master_file,directory):
    try:
        shutil.copy(master_file,os.path.join(directory,"image_id"+".jpg"))
        log.logger.debug('Succesfully copied master file to ' + directory)
    except Exception as e:
        log.logger.critical('Could not copy master file')
        log.logger.critical(e)
        exit(1)
