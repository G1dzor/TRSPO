from concurrent.futures import ThreadPoolExecutor
from time import time
from threading import Lock

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

def main():
    max_number = 10_000  # Максимальне число для обробки
    number_of_threads = 4  # Кількість потоків

    total_steps = 0
    count = 0
    total_steps_lock = Lock()  # Блокування для атомарних операцій
    count_lock = Lock()

    start_time = time()

    def task(number):
        nonlocal total_steps, count
        steps = compute_collatz_steps(number)
        with total_steps_lock:
            total_steps += steps
        with count_lock:
            count += 1

    # Використовуємо пул потоків
    with ThreadPoolExecutor(max_workers=number_of_threads) as executor:
        executor.map(task, range(1, max_number + 1))

    # Обчислення середньої кількості кроків
    average_steps = total_steps / count if count > 0 else 0

    end_time = time()
    print(f"Середня кількість кроків для виродження в 1: {average_steps}")
    print(f"Час виконання: {int((end_time - start_time) * 1000)} мс")

if __name__ == "__main__":
    main()
