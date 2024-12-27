import socket
import struct

def send_message(sock, message_type, message_body):
    """Надсилає повідомлення у форматі: [довжина][тип][тіло]"""
    body = message_body.encode() if isinstance(message_body, str) else struct.pack("d", message_body)
    header = struct.pack("I", len(body) + 1)  # Довжина = тип (1 байт) + тіло
    sock.sendall(header + struct.pack("B", message_type) + body)

def receive_message(sock):
    """Приймає повідомлення у форматі: [довжина][тип][тіло]"""
    # Читаємо заголовок
    header = sock.recv(4)
    while len(header) < 4:
        header += sock.recv(4 - len(header))
    length = struct.unpack("I", header)[0]

    # Читаємо тип повідомлення
    message_type = sock.recv(1)
    while len(message_type) < 1:
        message_type += sock.recv(1)
    message_type = struct.unpack("B", message_type)[0]

    # Читаємо тіло повідомлення
    body = b""
    while len(body) < length - 1:
        body += sock.recv(length - 1 - len(body))

    return message_type, body

def main():
    port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen(1)
            print("Сервер запущено, очікування підключення...")

            client_socket, client_address = server_socket.accept()
            print(f"Підключено клієнта: {client_address}")

            with client_socket:
                for i in range(100):
                    message_type, body = receive_message(client_socket)

                    if message_type == 1:
                        message_body = body.decode()
                    elif message_type == 2:
                        message_body = struct.unpack("I", body)[0]
                    else:
                        message_body = struct.unpack("d", body)[0]

                    print(f"Отримано повідомлення типу {message_type}: {message_body}")

                    # Формуємо відповідь
                    response_type = message_type
                    if message_type == 1:
                        response_body = f"Прийнято: {message_body}"
                    elif message_type == 2:
                        response_body = message_body * 2  # Ціле число
                    else:
                        response_body = message_body / 2  # Число з плаваючою комою

                    print(f"Відправляємо відповідь типу {response_type}: {response_body}")
                    send_message(client_socket, response_type, response_body)

    except Exception as e:
        print(f"Помилка сервера: {e}")

if __name__ == "__main__":
    main()
