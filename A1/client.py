import socket
s = socket.socket()
host = socket.gethostname()
port = 9999
address = (host, port)
msg = '/connect anotherchatroom'




s.connect(address)
s.send(msg)