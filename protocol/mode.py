def handle(sock, args, clients, server):
    # Команда MODE <target> <flags>
    if len(args) < 2: return
    
    target = args[0]
    mode = args[1]
    
    # Пока просто логируем изменение мода
    print(f"[MODE] {target} установил режим: {mode}")
    server.send_raw(sock, f":SERVER 324 {clients[sock]['nick']} {target} {mode} :Mode set")
