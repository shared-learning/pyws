from gevent import monkey
monkey.patch_all()

import cgi
import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
socketio = SocketIO(app)

@app.route("/")
def hello():
    return render_template('main.html')

@socketio.on('connect', namespace='/dd')
def ws_conn():
    c=db.incr('count')
    socketio.emit('msg', {'count': c}, namespace='/dd')

@socketio.on('disconnect', namespace='/dd')
def ws_disconn():
    c=db.decr('count')
    socketio.emit('msg', {'count': c}, namespace='/dd')

if __name__ == "__main__":
    socketio.run(app, '0.0.0.0', port=5000, debug=True)
