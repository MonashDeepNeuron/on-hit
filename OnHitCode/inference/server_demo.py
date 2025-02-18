import socket

server_ip = "0.0.0.0"  # Listen on all interfaces
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Server listening on {server_ip}:{server_port}...")

client_socket, client_address = server_socket.accept()
print(f"Connected by {client_address}")

# Receive data from client
data = client_socket.recv(8192).decode()
print(f"Received from client: {data}")

# Process and send a response
response = f"Server received: {data.upper()}"
client_socket.sendall(response.encode())

# Close sockets
client_socket.close()
server_socket.close()
