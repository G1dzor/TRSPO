import socket
from threading import Thread

def receive_messages(client_socket):
    """Функція для отримання повідомлень від клієнта."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("Клієнт завершив з'єднання.")
                break
            print(f"\nКлієнт: {message}")
        except Exception as e:
            print(f"Помилка отримання повідомлення: {e}")
            break

def main():
    port = 12345  # Порт, на якому працює сервер

    try:
        # Створення сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("0.0.0.0", port))
            server_socket.listen(5)
            print("Сервер запущено, очікування підключення...")

            # Приймаємо підключення клієнта
            client_socket, client_address = server_socket.accept()
            print(f"Підключено клієнта: {client_address}")

            with client_socket:
                # Запуск потоку для отримання повідомлень
                receiver_thread = Thread(target=receive_messages, args=(client_socket,), daemon=True)
                receiver_thread.start()

                while True:
                    # Ввід повідомлення для клієнта
                    message = input("\nВи: ")
                    client_socket.sendall(message.encode())

                    if message.lower() == "exit":
                        print("Завершення з'єднання.")
                        break

    except Exception as e:
        print(f"Помилка сервера: {e}")

if __name__ == "__main__":
    main()
