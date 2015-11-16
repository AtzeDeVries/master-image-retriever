from flask import Flask, render_template, send_file, redirect
from flask.ext.socketio import SocketIO, send, emit
import threading
import time
import os, shutil, re

from lib import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect', namespace='/mir')
def handle_message():
    log.logger.debug('user connected')
    #socketio.emit('newnumber', {'number': 'online'}, namespace='/mir')


@socketio.on('disconnect', namespace='/mir')
def handle_disconnect():
    log.logger.debug('user diconnected')


def get_query_status():
    status = mq.get('status:query',q)
    if status is None:
        return 'query process not running!'
    else:
        return status

def get_master_status():
    status = mq.get('status:master_file',q)
    if status is None:
        return 'master_file process not running!'
    else:
        return status

def check_downloads():
    status = mq.qsize('data:zip',q)
    if status < 1:
        return 'no downloads ready'
    else:
        return "<a href='/download'>download ready.</a>"

def cleanup(master_file):
    master_dir = os.path.dirname(master_file)
    keep = master_file.split("/")[-1]
    dirlist = os.listdir(master_dir)
    dirlist.remove(keep)
    if len(dirlist) > 0:
        for f in dirlist:
            fl = os.path.join(master_dir,f)
            log.logger.debug("cleanup of %s" % fl )
            if os.path.isfile(fl):
                os.remove(fl)
            else:
                shutil.rmtree(fl)

def check_errors():
    error_list = mq.pop('error:query',q)
    if not error_list is None:
        socketio.emit('errors', {'data': "</br>".join(error_list.split(","))}, namespace='/mir')

def run_download():
    if mq.qsize('data:zip',q) < 1:
        return render_template('download.html')
    else:
        filelink = mq.pop('data:zip',q)
        log.logger.debug("found file %s" % filelink)
        cwd = os.path.dirname(os.path.realpath("__file__"))
        fullpath = os.path.join(cwd,filelink)
        cleanup(fullpath)
        return send_file(fullpath,
                          mimetype='application/zip',
                          attachment_filename=fullpath.split("/")[-1],
                          as_attachment=True)

def ping_thread():
    count = 0
    while True:
        time.sleep(1)
        qstatus = get_query_status()
        mstatus = get_master_status()
        check_errors()
        dstatus = check_downloads()
        socketio.emit('querystatus', {'data': qstatus}, namespace='/mir')
        socketio.emit('filefind', {'data': mstatus}, namespace='/mir')
        socketio.emit('downloads', {'data': dstatus}, namespace='/mir')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def do_download():
    return run_download()

@socketio.on('getfiles', namespace='/mir')
def send_list(message):
    not_allowed = ['%'," AND ","CREATE","TABLE","DATABASE","INT","WHERE","DELETE"]
    if not message['data']:
        log.logger.warning("got no input")
    elif any(x in message['data'].upper() for x in not_allowed):
        log.logger.warning("input contains not allowed characters %s" % message['data'])
    else:
        log.logger.info("got input of %s" % message['data'])
        mq.put('data:regno_list',q,message['data'])
    #
    #emit('my respone', {'data': 'pet'})

if __name__ == '__main__':
    #setup redis connection
    q = mq.redis_connect()

    # run_download()
    # exit()
    #setup threaing
    t = threading.Thread(target=ping_thread)
    t.daemon = True
    t.start()
    # start socket webapp
    socketio.run(app)
