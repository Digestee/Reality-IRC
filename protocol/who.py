def handle(sock, args, clients, server):
    # Команда WHO <channel>
    target = args[0] if args else "*"
    nick = clients[sock]['nick']
    
    # RPL_WHOREPLY (352)
    # Формат: <channel> <user> <host> <server> <nick> <H|G> :<realname>
    for s, info in clients.items():
        if target == "*" or target in info.get('channels', []):
            user = info['user']
            server.send_raw(sock, f":SERVER 352 {nick} {target} {user} localhost irc.future.dev {info['nick']} H :0 RealName")
    
    # RPL_ENDOFWHO (315)
    server.send_raw(sock, f":SERVER 315 {nick} {target} :End of /WHO list.")
