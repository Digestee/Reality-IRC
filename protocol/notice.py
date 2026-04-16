def handle(sock, args, clients, server):
    if len(args) < 2: return
    target = args[0]
    msg = " ".join(args[1:]).lstrip(':')
    nick = clients[sock]['nick']
    
    out = f":{nick} NOTICE {target} :{msg}"
    
    if target.startswith('#'):
        server.broadcast(out, sock, channel=target)
    else:
        for s, info in clients.items():
            if info['nick'] == target:
                server.send_raw(s, out)
                break
