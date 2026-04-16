def handle(sock, args, clients, server):
    if not args:
        server.send_raw(sock, ":SERVER 431 :No nickname given")
        return
    
    target_nick = args[0]
    found = False
    
    for s, info in clients.items():
        if info['nick'] == target_nick:
            # RPL_WHOISUSER (311)
            server.send_raw(sock, f":SERVER 311 {info['nick']} {info['user']} localhost * :RealName")
            # RPL_WHOISCHANNELS (319)
            chans = " ".join(info['channels'])
            server.send_raw(sock, f":SERVER 319 {info['nick']} :{chans}")
            # RPL_ENDOFWHOIS (318)
            server.send_raw(sock, f":SERVER 318 {info['nick']} :End of /WHOIS list.")
            found = True
            break
            
    if not found:
        server.send_raw(sock, f":SERVER 401 {target_nick} :No such nick/channel")
