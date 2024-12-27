import socket
from threading import Thread

def receive_messages(client_socket):
    """Функція для отримання повідомлень від сервера."""
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print("З'єднання з сервером закрито.")
                break
            print(f"\nСервер: {message}")
        except Exception as e:
            print(f"Помилка отримання повідомлення: {e}")
            break

def main():
    server_address = "localhost"  # Адреса сервера
    port = 12345  # Порт сервера

    try:
        # Підключення до сервера
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, port))
            print("Підключено до сервера.")

            # Запуск потоку для отримання повідомлень
            receiver_thread = Thread(target=receive_messages, args=(client_socket,), daemon=True)
            receiver_thread.start()

            while True:
                # Ввід повідомлення для сервера
                message = input("\nВи: ")
                client_socket.sendall(message.encode())

                if message.lower() == "exit":
                    print("Завершення з'єднання.")
                    break

    except Exception as e:
        print(f"Помилка клієнта: {e}")

if __name__ == "__main__":
    main()
