import socket
import struct

def main():
    hostname = 'localhost'
    port = 8080

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((hostname, port))

            for i in range(100):
                # Створити та надіслати повідомлення
                message = f"Hello Server, message #{i + 1}"
                message_bytes = message.encode('utf-8')

                # Надіслати довжину повідомлення і саме повідомлення
                sock.sendall(struct.pack('!I', len(message_bytes)))
                sock.sendall(message_bytes)

                # Отримати відповідь від сервера
                response_length = struct.unpack('!I', sock.recv(4))[0]
                response_bytes = sock.recv(response_length)
                server_response = response_bytes.decode('utf-8')

                print(f"Received from server: {server_response}")

        print("Client finished communication")

    except Exception as ex:
        print(f"Client exception: {ex}")

if __name__ == '__main__':
    main()
