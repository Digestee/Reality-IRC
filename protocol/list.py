def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 321 {nick} Channel :Users  Name")
    # Пробегаемся по всем каналам, которые знают юзеры
    for chan in set(c for info in clients.values() for c in info['channels']):
        server.send_raw(sock, f":SERVER 322 {nick} {chan} 1 :Topic info")
    server.send_raw(sock, f":SERVER 323 {nick} :End of /LIST")
