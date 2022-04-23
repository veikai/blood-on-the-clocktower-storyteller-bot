#! -*- coding: utf-8 -*-
import asyncio
import websockets
from .game import game


# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_user_msg(websocket):
    while True:
        recv_str = await websocket.recv()
        message, index = recv_str.split("#")
        if message == "开始游戏":
            await game.start()
        elif message.startswith("action"):
            _, target = message.split("@")
            target = [int(_target) - 1 for _target in target.split(",")]
            await game.do_action(int(index) - 1, target)
        elif message == "下阶段":
            await game.next_stage()
        elif message.startswith("提名"):
            _, target = message.split("@")
            await game.nominate(int(index) - 1, int(target) - 1)
        elif message.startswith("投票"):
            _, target = message.split("@")
            await game.vote(int(index) - 1, int(target) - 1)
        elif message == "处决":
            await game.execute()
        # print("recv_text:", websocket.pong, recv_text)
        # response_text = f"Server return: {recv_text}"
        # print("response_text:", response_text)


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
