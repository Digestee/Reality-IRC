def handle(sock, args, clients, server):
    if args:
        # Устанавливаем Away
        away_msg = " ".join(args).lstrip(':')
        clients[sock]['away'] = away_msg
        server.send_raw(sock, f":SERVER 306 {clients[sock]['nick']} :You have been marked as being away")
    else:
        # Снимаем Away
        if 'away' in clients[sock]:
            del clients[sock]['away']
            server.send_raw(sock, f":SERVER 305 {clients[sock]['nick']} :You are no longer marked as being away")
