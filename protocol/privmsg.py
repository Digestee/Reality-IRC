def handle(sock, args, clients, server):
    if len(args) < 2: return
    target = args[0]
    text = " ".join(args[1:]).lstrip(':')
    nick = clients[sock]['nick']
    msg = f":{nick} PRIVMSG {target} :{text}"
    if target.startswith('#'):
        server.broadcast(msg, sock, channel=target)
    else:
        for s, info in clients.items():
            if info['nick'] == target:
                server.send_raw(s, msg)
                break
