from socket_server import *


server = SocketServer()
try:
    # message = server.receive_single_message()
    # print(f"Final message received: {message}")
    server.continuous_receive_return_message()
except KeyboardInterrupt:
    print("\nServer interrupted.")
finally:
    server.close_socket()