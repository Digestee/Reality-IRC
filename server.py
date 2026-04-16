import socket
import select
import os
import importlib.util

# Автоматически находим абсолютный путь к папке, где лежит server.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class CleanIRC:
    def __init__(self, port=6667):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind(('0.0.0.0', port))
        self.serv.listen(10)
        
        self.clients = {}  
        self.socks = [self.serv]
        self.commands = {}
        self.buffers = {} # Новое: Буфер для склеивания TCP-пакетов
        
        print(f"[*] Чистое ядро RFC 1459 запущено на порту {port}")

    def send_raw(self, sock, msg):
        try:
            sock.send((msg + "\r\n").encode('utf-8'))
        except: pass

    def broadcast(self, msg, sender_sock, channel=None):
        for s, info in self.clients.items():
            if s == sender_sock: continue
            if channel and channel not in info['channels']: continue
            self.send_raw(s, msg)

    def parse_irc(self, data):
        if not data: return None, []
        if " :" in data:
            args_part, trailing = data.split(" :", 1)
            args = args_part.split()
            args.append(trailing)
        else:
            args = data.split()
            
        if not args: return None, []
        cmd = args[0].lower()
        return cmd, args[1:]

    def handle_command(self, sock, data):
        cmd, args = self.parse_irc(data)
        if not cmd: return

        # Новое: Защита от Path Traversal. Команда должна состоять только из букв!
        if not cmd.isalpha():
            self.send_raw(sock, f":SERVER 421 {cmd.upper()} :Invalid command format")
            return

        if cmd not in self.commands:
            path = os.path.join(BASE_DIR, "protocol", f"{cmd}.py")
            if os.path.exists(path):
                spec = importlib.util.spec_from_file_location(cmd, path)
                m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(m)
                self.commands[cmd] = m
            else:
                self.send_raw(sock, f":SERVER 421 {cmd.upper()} :Unknown command")
                return

        try:
            self.commands[cmd].handle(sock, args, self.clients, self)
        except Exception as e:
            print(f"[!] Ошибка в команде {cmd}: {e}")

    def run(self):
        while True:
            r, _, _ = select.select(self.socks, [], [])
            for s in r:
                if s is self.serv:
                    conn, addr = s.accept()
                    self.socks.append(conn)
                    self.clients[conn] = {
                        'nick': '*', 'user': '*', 'reg': False, 
                        'channels': [], 'host': addr[0]
                    }
                    self.buffers[conn] = "" # Новое: инициализируем пустой буфер для клиента
                    print(f"[*] Новое соединение: {addr[0]}")
                else:
                    try:
                        data = s.recv(1024).decode('utf-8', errors='ignore')
                        if not data: raise Exception("Disconnected")
                        
                        # Новое: Правильная обработка потока TCP
                        self.buffers[s] += data
                        while '\n' in self.buffers[s]:
                            # Отрезаем одну строку до \n, остаток оставляем в буфере
                            line, self.buffers[s] = self.buffers[s].split('\n', 1)
                            line = line.strip()
                            if line:
                                print(f"[DEBUG] <- {line}")
                                self.handle_command(s, line)
                    except:
                        self.disconnect(s)

    def disconnect(self, sock):
        if sock in self.clients:
            nick = self.clients[sock]['nick']
            print(f"[*] Клиент {nick} отключился")
            del self.clients[sock]
        
        # Новое: Очищаем буфер при отключении
        if sock in self.buffers:
            del self.buffers[sock]
            
        if sock in self.socks:
            self.socks.remove(sock)
        sock.close()

if __name__ == "__main__":
    CleanIRC().run()
