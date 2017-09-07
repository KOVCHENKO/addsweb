import pickle,socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.setblocking(1)
sock.connect('/tmp/navgps')


navdata = pickle.loads(sock.recv(1024))

print navdata

