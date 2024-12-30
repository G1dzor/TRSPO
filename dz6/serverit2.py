import socket
import struct

def main():
    port = 8080

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', port))
            server_socket.listen(1)
            print(f"Server is listening on port {port}")

            conn, addr = server_socket.accept()
            with conn:
                print(f"Client connected from {addr}")

                for i in range(100):
                    # Отримати довжину повідомлення
                    message_length = struct.unpack('!I', conn.recv(4))[0]

                    # Отримати саме повідомлення
                    message_bytes = conn.recv(message_length)
                    received_message = message_bytes.decode('utf-8')

                    print(f"Received from client: {received_message}")

                    # Відповісти клієнту
                    response_message = f"Message {i + 1} received"
                    response_bytes = response_message.encode('utf-8')

                    # Надіслати довжину відповіді і саму відповідь
                    conn.sendall(struct.pack('!I', len(response_bytes)))
                    conn.sendall(response_bytes)

            print("Server finished communication")

    except Exception as ex:
        print(f"Server exception: {ex}")

if __name__ == '__main__':
    main()
