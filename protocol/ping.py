def handle(sock, args, clients, server):
    server.send_raw(sock, f"PONG {' '.join(args)}")
