import socket
import threading
import json
from game_core import GomokuGame
from opengl_renderer import OpenGLRenderer
import pygame

'''
    这里使用Socket通信来实现服务端（server）和客户端（client）的连接
    直接调用socket库提供的高层API接口，所以自没有定义SYN,ACK等包
    服务端和客户端均由一个渲染的主线程和用于接受消息的子线程
'''

# 初始化
class NetworkGame:
    def __init__(self, is_server=False, host="127.0.0.1", port=5555):
        self.game = GomokuGame()
        self.renderer = OpenGLRenderer(self.game)
        self.is_server = is_server   #bool 类型
        self.host = host
        self.port = port
        self.sock = None
        self.connection = None
        self.running = True
        self.my_turn = is_server  # 服务器先手
# 启动服务器
    def start_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建TCP套接字
        self.sock.bind((self.host, self.port))   # 绑定地址和端口
        self.sock.listen(1)  # 开始监听
        print(f"服务器已启动，等待连接...")
        self.connection, addr = self.sock.accept()  # 接受客户端连接  （三次握手完成）
        print(f"客户端已连接: {addr}")
        self.start_receive_thread()
# 连接服务器
    def connect_to_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 套接字
        self.sock.connect((self.host, self.port))      # 连接服务器（发起三次握手）
        print("已连接到服务器")
        self.connection = self.sock
        self.start_receive_thread()
# 新启动一个线程来接受网络消息，防止界面阻塞主线程
    def start_receive_thread(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while self.running:
            try:
                data = self.connection.recv(1024).decode('utf-8')
                if not data:
                    break

                message = json.loads(data)
                self.handle_message(message)
            except Exception as e:
                print(f"接收错误: {e}")
                break
# 落子信息（包含行列坐标）
    def handle_message(self, message):
        if message['type'] == 'move':
            row, col = message['move']
            self.game.make_move(row, col)
            self.my_turn = True
        elif message['type'] == 'reset':
            self.game.reset_game()
            self.my_turn = self.is_server

    def send_move(self, row, col):
        if not self.connection:
            return

        message = {
            'type': 'move',
            'move': (row, col)
        }
        self.connection.send(json.dumps(message).encode('utf-8'))
        self.my_turn = False

    def send_reset(self):
        if not self.connection:
            return

        message = {'type': 'reset'}
        self.connection.send(json.dumps(message).encode('utf-8'))

    def run(self):
        if self.is_server:
            self.start_server()
        else:
            self.connect_to_server()

        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.game.game_over and self.my_turn and self.renderer.is_click_on_board(event.pos):
                        row, col = self.renderer.screen_to_board(event.pos)
                        if self.game.make_move(int(row), int(col)):
                            self.send_move(row, col)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 重置游戏
                        self.game.reset_game()
                        if self.is_server:
                            self.my_turn = True
                        else:
                            self.my_turn = False
                        self.send_reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            self.renderer.render()
            clock.tick(60)

        if self.connection:
            self.connection.close()
        if self.sock:
            self.sock.close()
        pygame.quit()