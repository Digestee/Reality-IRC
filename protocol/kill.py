def handle(sock, args, clients, server):
    if clients[sock].get('mode') != '+o':
        server.send_raw(sock, ":SERVER 481 :Permission Denied- You're not an IRC operator")
        return

    if len(args) < 1:
        server.send_raw(sock, ":SERVER 461 KILL :Not enough parameters")
        return

    target_nick = args[0]
    reason = " ".join(args[1:]).lstrip(':') if len(args) > 1 else "No reason"

    # Ищем цель
    for s, info in list(clients.items()): # list() чтобы безопасно удалять во время цикла
        if info['nick'] == target_nick:
            try:
                s.send(f"ERROR :Closing link: {target_nick} (Killed by {clients[sock]['nick']}: {reason})\r\n".encode())
            except: pass
            
            print(f"[!] {clients[sock]['nick']} УБИЛ {target_nick}. Причина: {reason}")
            server.disconnect(s)  # <-- ИСПОЛЬЗУЕМ ЯДРО!
            return
            
    server.send_raw(sock, f":SERVER 401 {target_nick} :No such nick/channel")
