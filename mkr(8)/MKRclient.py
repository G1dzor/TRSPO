import socket
import random
import struct

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

def generate_matrix(rows, cols):
    return [[random.randint(0, 99) for _ in range(cols)] for _ in range(rows)]

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            client_socket.settimeout(10)  # Set 10-second timeout
            output_stream = client_socket.makefile('wb')
            input_stream = client_socket.makefile('rb')

            # Generate random dimensions for matrices
            N = random.randint(1000, 1999)
            M = random.randint(1000, 1999)
            L = random.randint(1000, 1999)

            print(f"Generated matrices: A({N}x{M}), B({M}x{L})")

            # Generate matrices A and B
            matrixA = generate_matrix(N, M)
            matrixB = generate_matrix(M, L)

            # Send dimensions to the server
            print(f"Sending dimensions: N={N}, M={M}, L={L}")
            output_stream.write(struct.pack('!I', N))
            output_stream.write(struct.pack('!I', M))
            output_stream.write(struct.pack('!I', L))

            # Send matrix A
            print("Sending matrix A...")
            for row in matrixA:
                for value in row:
                    output_stream.write(struct.pack('!I', value))

            # Send matrix B
            print("Sending matrix B...")
            for row in matrixB:
                for value in row:
                    output_stream.write(struct.pack('!I', value))

            # Receive result matrix
            result_matrix = []
            print("Receiving result matrix...")
            for i in range(N):
                row = []
                for j in range(L):
                    value = struct.unpack('!I', input_stream.read(4))[0]
                    row.append(value)
                result_matrix.append(row)

            print("Matrix multiplication result received.")
    except Exception as e:
        print(f"Client exception: {e}")

if __name__ == "__main__":
    main()
