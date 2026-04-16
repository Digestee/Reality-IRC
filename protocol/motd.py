def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 375 {nick} :- irc.future.dev Message of the day")
    server.send_raw(sock, f":SERVER 372 {nick} :- --------------------------------")
    server.send_raw(sock, f":SERVER 372 {nick} :- Reality-Messenger 2026 Ready")
    server.send_raw(sock, f":SERVER 372 {nick} :- --------------------------------")
    server.send_raw(sock, f":SERVER 376 {nick} :End of /MOTD command")
