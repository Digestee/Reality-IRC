def handle(sock, args, clients, server):
    nick = clients[sock]['nick']
    server.send_raw(sock, f":SERVER 256 {nick} :Administrative info")
    server.send_raw(sock, f":SERVER 257 {nick} :City: Termux/Android")
    server.send_raw(sock, f":SERVER 258 {nick} :Email: reality@irc.future.dev")
