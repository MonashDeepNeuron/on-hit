import socket
import asyncio
import concurrent.futures
from typing import (Any)

class SocketClient:
    '''
    Use this on the remote computer to send messages to a socket
    Input:
        server_ip: str = ip address
        port:int = port number used to connect to
    '''
    def __init__(self, server_ip:str="130.194.132.217", port:int=5000):
        self.server_ip = server_ip
        self.server_port = port
        self.is_connected = False
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)
        self.client_socket.connect((self.server_ip, self.server_port))
        print(f"Connected to {self.server_ip}:{self.server_port}")

    async def connect(self) -> bool:
        """Establish connection if not already connected"""
        if not self.is_connected:
            try:
                self.client_socket = await asyncio.to_thread(self._create_socket)
                self.is_connected = True
                print(f"[SOCKET] Connected to {self.server_ip}:{self.server_port}")
                return True
            except Exception as e:
                print(f"[SOCKET] Connection error: {str(e)}")
                return False

        return True

    def _create_socket(self) -> socket.socket:
        """Create socket connection in a thread"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((self.server_ip, self.server_port))
        return sock

    async def send_and_receive_message(self, message: Any) -> str:
        """Send message and receive response"""
        # If there is no current connection
        if not self.is_connected:
            await self.connect()
            if not self.is_connected:
                return "Connection failed"

        try:
            return asyncio.to_thread(lambda: self._send_and_receive(message))
        except Exception as e:
            print(f"[SOCKET] Send message error: {str(e)}")
            self.is_connected = False
            print("[SOCKET] Attempting reconnect..")

            # Attempt reconnect
            await self.connect()
            if self.is_connected:
                print("[SOCKET] Connection success")
                try:
                    # Attempt to resend/receive data
                    return asyncio.to_thread(lambda: self._send_and_receive(message))
                except Exception as e2:
                    # Second attempt failed.
                    print(f"[SOCKET] Send message failed: {str(e2)}")
                    return f"Error: {str(e2)}"

            print(f"[SOCKET] Reconnection failed: {str(e)}")
            return f"Error: {str(e)}"

    def _send_and_receive(self, message: Any) -> str:
        """Send and receive message in a thread

        Parameter:
            message (any): Payload message to send over to client

        Returns:
            str: Response from the client
        """
        if not self.client_socket:
            raise RuntimeError("Socket is not initialised")

        print(f"[SOCKET] Sending data to backend..")
        self.client_socket.sendall(message)
        response = self.client_socket.recv(1024).decode()
        print(f"[SOCKET] Received response from backend")
        return response

    async def close(self) -> None:
        """Close socket connection"""
        if self.is_connected and self.client_socket:
            await asyncio.to_thread(self._close_socket)
            self.is_connected = False
            self.client_socket = None

    def _close_socket(self) -> None:
        """Close socket connection in a thread"""
        if self.client_socket:
            self.client_socket.close()
            print("[SOCKET] Socket connection closed")

async def _test(server_ip: str, port: int):
    """
    Send one message and receives a message from the client.
    Used for testing purposes
    """
    client = SocketClient(server_ip, port)  # Replace with actual server IP
    try:
        await client.send_and_receive_message("Hello, Server!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.close()

# Run the client to send one message
if __name__ == "__main__":
    asyncio.run(_test("130.194.132.217", 5000))
