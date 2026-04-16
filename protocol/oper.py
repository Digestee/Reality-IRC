def handle(sock, args, clients, server):
    if len(args) < 2:
        server.send_raw(sock, ":SERVER 461 OPER :Not enough parameters")
        return
    
    user, password = args[0], args[1]
    
    # Секретный пароль для админки (можно вынести в конфиг)
    if password == "admin123":
        clients[sock]['mode'] = '+o' # Добавляем флаг оператора
        server.send_raw(sock, ":SERVER 381 :You are now an IRC operator")
        print(f"[!] {clients[sock]['nick']} стал ОПЕРАТОРОМ")
    else:
        server.send_raw(sock, ":SERVER 464 :Password incorrect")
