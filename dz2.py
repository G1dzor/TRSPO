import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time

def compute_collatz_steps(n):
    """Обчислює кількість кроків за гіпотезою Колаца."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def producer_task(task_queue, max_number, number_of_threads):
    """Додає числа до черги для обробки."""
    for i in range(1, max_number + 1):
        task_queue.put(i)
    for _ in range(number_of_threads):
        task_queue.put(-1)  # Маркер завершення
    print("Усі числа додані до черги.")

def consumer_task(task_queue, results_queue):
    """Обчислює кроки за гіпотезою Колаца для чисел з черги."""
    while True:
        number = task_queue.get()
        if number == -1:
            break
        steps = compute_collatz_steps(number)
        results_queue.put(steps)
        if number % 1000 == 0:
            print(f"Оброблено число: {number}")

def calculate_average_steps(results_queue):
    """Підраховує середню кількість кроків за результатами в черзі."""
    total_steps = 0
    count = 0
    while not results_queue.empty():
        total_steps += results_queue.get()
        count += 1
    print(f"Оброблено результатів: {count}")
    return total_steps / count if count > 0 else 0

def main():
    number_of_threads = 4  # Кількість потоків
    max_number = 10_000  # Максимальне число для обробки

    task_queue = Queue()
    results_queue = Queue()

    start_time = time.time()

    # Запуск потоків продюсера і споживачів
    with ThreadPoolExecutor(max_workers=number_of_threads + 1) as executor:
        executor.submit(producer_task, task_queue, max_number, number_of_threads)
        for _ in range(number_of_threads):
            executor.submit(consumer_task, task_queue, results_queue)

    # Обчислення середньої кількості кроків
    average_steps = calculate_average_steps(results_queue)

    end_time = time.time()
    print(f"Середня кількість кроків для виродження в 1: {average_steps}")
    print(f"Час виконання: {int((end_time - start_time) * 1000)} мс")

if __name__ == "__main__":
    main()
