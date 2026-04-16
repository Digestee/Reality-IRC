def handle(sock, args, clients, server):
    if not args: return
    channel = args[0]
    nick = clients[sock]['nick']
    
    # Если тема не указана, сервер возвращает текущую (стр. 23)
    if len(args) == 1:
        topic = getattr(server, 'topics', {}).get(channel, "No topic is set")
        server.send_raw(sock, f":SERVER 332 {nick} {channel} :{topic}")
    else:
        # Установка новой темы
        new_topic = " ".join(args[1:]).lstrip(':')
        if not hasattr(server, 'topics'): server.topics = {}
        server.topics[channel] = new_topic
        
        # Уведомляем всех
        msg = f":{nick} TOPIC {channel} :{new_topic}"
        server.broadcast(msg, sock, channel=channel)
        server.send_raw(sock, msg)
