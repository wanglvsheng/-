import socket

phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

phone.bind(('127.0.0.1', 7979))

phone.listen(5)
print('服务端启动完成，监听地址为:%s:%s' % ('127.0.0.1', 8080))


# print("客户端的ip和端口：", c_addr)
while 1:
    conn, c_addr = phone.accept()
    while 1:
        try:
            info = conn.recv(1024)
            print(info.decode('utf-8'))
            conn.send(info.upper())
        except Exception:
            break

    conn.close()
phone.close()