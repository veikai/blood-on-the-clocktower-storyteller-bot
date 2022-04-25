from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect, send
from engineio.payload import Payload
from .TroubleBrewing import game


Payload.max_decode_packets = 50
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "eventlet"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def my_ping():
    emit('my_pong')


@socketio.event
def connect():
    player = game.add_player(request.sid)
    send(f"欢迎来到钟楼#{player.name}")
    send(f"玩家 {player.name} 加入游戏", broadcast=True)
    emit("player_index", player.name)


@socketio.event
def start_game():
    game.start()


def parse_command(command_str):
    commands = command_str.split("@")
    if commands.__len__() == 2:
        if not commands[1]:
            return commands[0], []
        else:
            targets = commands[1].split(",")
            return commands[0], targets
    else:
        return commands[0], []


@socketio.event
def command(command_str):
    command_, targets = parse_command(command_str)
    if command_ == "start game":
        game.start()
    elif command_.startswith("action"):
        game.do_action(request.sid, targets)
    elif command_ == "next stage":
        game.next_stage()
    elif command_.startswith("nominate"):
        if targets:
            game.nominate(request.sid, targets[0])
    elif command_.startswith("vote"):
        if targets:
            game.vote(request.sid, targets[0])
    elif command_ == "execute":
        game.execute()
    elif command_.startswith("shoot"):
        if targets:
            game.shoot(request.sid, targets[0])
    else:
        print("unknown command", command)


@socketio.on('disconnect')
def test_disconnect():
    game.remove_player(request.sid)
    print('Client disconnected', request.sid)


def start():
    socketio.run(app, host="0.0.0.0")


if __name__ == '__main__':
    start()
