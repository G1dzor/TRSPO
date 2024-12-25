print("Hello World") #step3
print("Привіт Світ") #step5
#step8
import threading
import time

# Функція для обчислення квадратів чисел
def calculate_squares(numbers):
    for n in numbers:
        print(f"Квадрат {n} дорівнює {n**2}\n")
        time.sleep(0.5)  # Затримка для симуляції роботи

# Функція для обчислення кубів чисел
def calculate_cubes(numbers):
    for n in numbers:
        print(f"Куб {n} дорівнює {n**3}\n")
        time.sleep(0.5)  # Затримка для симуляції роботи

# Список чисел для обчислення
numbers = [1, 2, 3, 4, 5]

# Створення потоків
thread1 = threading.Thread(target=calculate_squares, args=(numbers,))
thread2 = threading.Thread(target=calculate_cubes, args=(numbers,))

# Запуск потоків
thread1.start()
thread2.start()

# Очікування завершення потоків
thread1.join()
thread2.join()

print("Обчислення завершено.")
