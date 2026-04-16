def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 364 {nick} irc.future.dev irc.future.dev :0 Info")
    server.send_raw(sock, f":SERVER 365 {nick} irc.future.dev :End of /LINKS")
