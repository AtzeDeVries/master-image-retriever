from flask import Flask, render_template
from flask.ext.socketio import SocketIO, send, emit
import threading
import time

from lib import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('connect', namespace='/mir')
def handle_message():
    print 'connected'
    #socketio.emit('newnumber', {'number': 'online'}, namespace='/mir')

@app.route('/')
def index():
    return render_template('index.html')

def get_query_status():
    status = mq.get('status:query',q)
    if status is None:
        return 'query process not running!'
    else:
        return status

def ping_thread():
    count = 0
    while True:
        time.sleep(1)
        qstatus = get_query_status()
        print qstatus
        socketio.emit('newnumber', {'number': qstatus}, namespace='/mir')
        socketio.emit('filefind', {'data': 'found!'}, namespace='/mir')

if __name__ == '__main__':
    #setup redis connection
    q = mq.redis_connect()
    #setup threaing
    t = threading.Thread(target=ping_thread)
    t.daemon = True
    t.start()
    # start socket webapp
    socketio.run(app)
