#! -*- coding: utf-8 -*-
import asyncio
import websockets
from .TroubleBrewing import game


def parse_command(command):
    commands = command.split("@")
    if commands.__len__() == 2:
        targets = []
        for target in command[1].split(","):
            try:
                targets.append(int(target) - 1)
            except ValueError:
                pass
            except Exception as e:
                print(e)
        return commands[0], targets
    else:
        return commands[0], []


async def recv_user_msg(websocket):
    while True:
        recv_str = await websocket.recv()
        command, index = recv_str.split("#")
        player_index = int(index) - 1
        command, targets = parse_command(command)
        if command == "开始游戏":
            await game.start()
        elif command.startswith("action"):
            await game.do_action(player_index, targets)
        elif command == "下阶段":
            await game.next_stage()
        elif command.startswith("提名"):
            await game.nominate(player_index, targets[0])
        elif command.startswith("投票"):
            await game.vote(player_index, targets[0])
        elif command == "处决":
            await game.execute()
        else:
            print("unknown command", command)


# 服务器端主逻辑
async def run(websocket, path):
    await game.add_player(websocket)
    await websocket.send(f"欢迎来到血染钟楼#{game.players.__len__()}")
    while True:
        try:
            await recv_user_msg(websocket)
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)  # 链接断开
            break
        except websockets.InvalidState:
            print("InvalidState...")  # 无效状态
            break
        except Exception as e:
            print("Exception:", e)
            raise


def start():
    print("127.0.0.1:8181 websocket...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.serve(run, "127.0.0.1", 8181))
    loop.run_forever()


if __name__ == '__main__':
    start()
