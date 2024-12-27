import socket
import struct
import random
import time

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
    server_address = "localhost"
    port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, port))
            print("Підключено до сервера.")

            for i in range(100):
                # Випадково обираємо тип повідомлення
                message_type = random.choice([1, 2, 3])
                if message_type == 1:
                    message_body = f"Повідомлення {i}"  # Текст
                elif message_type == 2:
                    message_body = random.randint(0, 100)  # Ціле число
                else:
                    message_body = random.uniform(0, 100)  # Число з плаваючою комою

                print(f"Відправляємо повідомлення типу {message_type}: {message_body}")
                send_message(client_socket, message_type, message_body)

                # Приймаємо відповідь
                message_type, body = receive_message(client_socket)
                if message_type == 1:
                    response = body.decode()
                elif message_type == 2:
                    response = struct.unpack("I", body)[0]
                else:
                    response = struct.unpack("d", body)[0]

                print(f"Отримано відповідь типу {message_type}: {response}")

                time.sleep(0.1)  # Затримка для демонстрації

    except Exception as e:
        print(f"Помилка клієнта: {e}")

if __name__ == "__main__":
    main()
