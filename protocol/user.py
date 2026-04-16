def handle(sock, args, clients, server):
    if len(args) < 4:
        server.send_raw(sock, ":SERVER 461 USER :Not enough parameters")
        return
    clients[sock]['user'] = args[0]
    nick = clients[sock]['nick']
    if nick != '*' and not clients[sock]['reg']:
        clients[sock]['reg'] = True
        server.send_raw(sock, f":SERVER 001 {nick} :Welcome to the Internet Relay Network")
