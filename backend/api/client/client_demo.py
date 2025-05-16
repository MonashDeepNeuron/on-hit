import socket

server_ip = "127.0.1.1"
server_port = 5000 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip,server_port))

#send data to server
message = "hello world comp 1"
client_socket.sendall(message.encode())


#recieve response
response = client_socket.recv(8192).decode()
print(response)


client_socket.close()

