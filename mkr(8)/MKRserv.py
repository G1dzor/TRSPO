import socket
import struct
import threading
from concurrent.futures import ThreadPoolExecutor

SERVER_HOST = 'localhost'
SERVER_PORT = 8080
THREAD_POOL_SIZE = 16  # Кількість потоків у пулі для паралельного обчислення


def handle_client(client_socket):
    try:
        # Create input and output streams for the client connection
        input_stream = client_socket.makefile('rb')
        output_stream = client_socket.makefile('wb')

        # Receive dimensions (N, M, L)
        N = struct.unpack('!I', input_stream.read(4))[0]
        M = struct.unpack('!I', input_stream.read(4))[0]
        L = struct.unpack('!I', input_stream.read(4))[0]

        print(f"Received dimensions: N={N}, M={M}, L={L}")

        # Validate dimensions
        if M <= 0 or N <= 0 or L <= 0:
            output_stream.write(struct.pack('!I', -1))  # Invalid dimensions flag
            client_socket.close()
            return

        # Receive matrix A
        matrixA = []
        print("Receiving matrix A...")
        for i in range(N):
            row = []
            for j in range(M):
                value = struct.unpack('!I', input_stream.read(4))[0]
                row.append(value)
            matrixA.append(row)

        # Receive matrix B
        matrixB = []
        print("Receiving matrix B...")
        for i in range(M):
            row = []
            for j in range(L):
                value = struct.unpack('!I', input_stream.read(4))[0]
                row.append(value)
            matrixB.append(row)

        # Perform matrix multiplication using ThreadPoolExecutor
        print("Performing matrix multiplication...")
        result_matrix = multiply_matrices(matrixA, matrixB, N, M, L)

        # Send result matrix back to client
        print("Sending result matrix...")
        for row in result_matrix:
            for value in row:
                output_stream.write(struct.pack('!I', value))

        print("Result matrix sent to client.")
        client_socket.close()

    except Exception as e:
        print(f"Error handling client: {e}")
        client_socket.close()


def multiply_matrices(matrixA, matrixB, N, M, L):
    # Result matrix initialized with zeros
    result = [[0] * L for _ in range(N)]

    # Using ThreadPoolExecutor for parallel computation of each row
    with ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE) as executor:
        futures = []

        # Create a future for each row multiplication task
        for i in range(N):
            futures.append(executor.submit(compute_row, matrixA, matrixB, result, i, M, L))

        # Wait for all tasks to complete
        for future in futures:
            future.result()  # Blocks until the result is available

    return result


def compute_row(matrixA, matrixB, result, i, M, L):
    # Compute one row of the result matrix
    for j in range(L):
        value = 0
        for k in range(M):
            value += matrixA[i][k] * matrixB[k][j]
        result[i][j] = value


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server running on {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, _ = server_socket.accept()
            print("New client connected")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()


if __name__ == "__main__":
    start_server()
