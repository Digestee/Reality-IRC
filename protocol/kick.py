def handle(sock, args, clients, server):
    if len(args) < 2: return
    channel = args[0]
    target_nick = args[1]
    reason = " ".join(args[2:]).lstrip(':') if len(args) > 2 else "No reason"
    
    sender_nick = clients[sock]['nick']
    msg = f":{sender_nick} KICK {channel} {target_nick} :{reason}"
    
    # Шлем всем в канале
    server.broadcast(msg, sock, channel=channel)
    server.send_raw(sock, msg)
    
    # Удаляем цель из канала
    for s, info in clients.items():
        if info['nick'] == target_nick and channel in info['channels']:
            info['channels'].remove(channel)
