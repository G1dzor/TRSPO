import socket

def main():
    port = 12345  # Порт, на якому працює сервер

    try:
        # Створення сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen(5)
            print("Сервер запущено, очікування підключення...")

            while True:
                # Очікування підключення клієнта
                client_socket, client_address = server_socket.accept()
                print(f"Підключено клієнта: {client_address}")

                with client_socket:
                    # Отримання повідомлення від клієнта
                    message = client_socket.recv(1024).decode()
                    print(f"Отримано повідомлення: {message}")

                    # Відправлення відповіді клієнту
                    response = f"Сервер отримав ваше повідомлення: {message}"
                    client_socket.sendall(response.encode())
                    print("Відповідь надіслано.")

    except Exception as e:
        print(f"Помилка сервера: {e}")

if __name__ == "__main__":
    main()
