def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    total = len(clients)
    server.send_raw(sock, f":SERVER 251 {nick} :There are {total} users and 0 services on 1 servers")
    server.send_raw(sock, f":SERVER 255 {nick} :I have {total} clients and 1 servers")
