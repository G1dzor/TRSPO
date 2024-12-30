import socket

def main():
    server_address = "localhost"  # Адреса сервера
    port = 12345  # Порт сервера

    try:
        # Підключення до сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, port))
            print("Підключено до сервера.")

            # Відправлення повідомлення серверу
            message = "Привіт, сервере!"
            client_socket.sendall(message.encode())
            print(f"Надіслано повідомлення: {message}")

            # Отримання відповіді від сервера
            response = client_socket.recv(1024).decode()
            print(f"Отримано відповідь від сервера: {response}")

    except Exception as e:
        print(f"Помилка клієнта: {e}")

if __name__ == "__main__":
    main()
