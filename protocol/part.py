def handle(sock, args, clients, server):
    if not args:
        # Ошибка 461: ERR_NEEDMOREPARAMS (стр. 46)
        server.send_raw(sock, ":SERVER 461 PART :Not enough parameters")
        return
    
    channel = args[0]
    nick = clients[sock]['nick']
    
    # 1. Проверка, был ли юзер в канале (Ошибка 442: ERR_NOTONCHANNEL, стр. 45)
    if channel not in clients[sock]['channels']:
        server.send_raw(sock, f":SERVER 442 {channel} :You're not on that channel")
        return

    # 2. Удаляем канал из списка юзера
    clients[sock]['channels'].remove(channel)
    
    # 3. Уведомляем всех в канале, что юзер ушел (стр. 21)
    msg = f":{nick}!~{clients[sock]['user']}@localhost PART {channel}"
    server.send_raw(sock, msg)
    server.broadcast(msg, sock, channel=channel)
