def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 371 {nick} :Reality-Messenger v0.1 (Experimental)")
    server.send_raw(sock, f":SERVER 374 {nick} :End of /INFO list")
