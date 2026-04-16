def handle(sock, args, clients, server):
    reason = " ".join(args).lstrip(':') if args else "Client Quit"
    nick = clients[sock]['nick']
    
    # Сообщаем всем участникам каналов, что юзер ушел
    msg = f":{nick} QUIT :{reason}"
    server.broadcast(msg, sock)
    
    # Отправляем сообщение об ошибке/закрытии самому клиенту
    try:
        sock.send(f"ERROR :Closing link: {nick} ({reason})\r\n".encode())
    except:
        pass
        
    # Делегируем всю чистку (удаление из socks, clients, закрытие) ядру!
    server.disconnect(sock)
