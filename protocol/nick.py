def handle(sock, args, clients, server):
    if not args:
        server.send_raw(sock, ":SERVER 431 :No nickname given")
        return
    new_nick = args[0]
    # Проверка на дубликат (ERR_NICKNAMEINUSE 433)
    for s, info in clients.items():
        if info['nick'] == new_nick:
            server.send_raw(sock, f":SERVER 433 * {new_nick} :Nickname is already in use")
            return
    clients[sock]['nick'] = new_nick
    if clients[sock]['user'] != '*' and not clients[sock]['reg']:
        clients[sock]['reg'] = True
        server.send_raw(sock, f":SERVER 001 {new_nick} :Welcome to the Internet Relay Network")
