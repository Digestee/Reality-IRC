def handle(sock, args, clients, server):
    target_chan = args[0] if args else None
    nick = clients[sock]['nick']
    
    # RPL_NAMREPLY (353)
    nicks_in_chan = []
    for s, info in clients.items():
        if not target_chan or target_chan in info['channels']:
            nicks_in_chan.append(info['nick'])
            
    reply = f":SERVER 353 {nick} = {target_chan or '*'} :{' '.join(nicks_in_chan)}"
    server.send_raw(sock, reply)
    
    # RPL_ENDOFNAMES (366)
    server.send_raw(sock, f":SERVER 366 {nick} {target_chan or '*'} :End of /NAMES list.")
