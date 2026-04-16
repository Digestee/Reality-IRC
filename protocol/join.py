def handle(sock, args, clients, server):
    if not args: return
    channel = args[0]
    if not channel.startswith('#'): channel = '#' + channel
    
    # Чтобы не дублировать каналы, если юзер уже там
    if channel not in clients[sock]['channels']:
        clients[sock]['channels'].append(channel)
        
    nick = clients[sock]['nick']
    
    # 1. Уведомляем всех в канале, включая самого юзера
    msg = f":{nick} JOIN {channel}"
    server.send_raw(sock, msg)
    server.broadcast(msg, sock, channel=channel)
    
    # Новое: Изящное решение по RFC 1459. 
    # Заставляем сервер "сымитировать" вызов команд TOPIC и NAMES 
    # от лица этого пользователя, используя твои же модули!
    server.handle_command(sock, f"TOPIC {channel}")
    server.handle_command(sock, f"NAMES {channel}")
