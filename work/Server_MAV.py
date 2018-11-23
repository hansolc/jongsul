import socketserver
from os.path import exists
import sys
import os
import time

HOST = ''
PORT = 9999

number = 1 

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global number

        data_transferred = 0
        print('[%s] ' %self.client_address[0])
        filename = self.request.recv(1024)
        filename = filename.decode()

        # 서버에서 명령어 실행
        os.system('python3 ../synthesizer.py --load_path ../logs/son_2018-10-26_21-17-45 --text="%s"' %filename)

        print('파일 alarm 전송시작...')
        with open('samples/alarm'+str(number)+'.manual.wav', 'rb') as f:					## 이진파일 읽기모드로 open
            try:
                data = f.read(1024)
                while data:
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
        print('전송완료[%s]' % filename)
        number = number+1
        print(number)

def runServer():
    print('-----------파일 생성대기--------------')
    
    try:
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('서버 종료')

runServer()
