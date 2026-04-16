def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 351 {nick} Reality-IRC.2026 irc.future.dev :Running on Android/Termux")
