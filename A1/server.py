import socket
s = socket.socket()
host = socket.gethostname()
port = 9999
address = (host, port)
print('Starting Server...')
s.bind(address)
s.listen(5)
while True:
 client, addr = s.accept()
 data = client.recv(1024)
 print('%s:%s says >> %s' % (addr[0], addr[1], data))
