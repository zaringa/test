import socket
import os
import argparse
from typing import Tuple

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="TCP Server for file transfer.")
    parser.add_argument("file_path", help="Path to the file to serve.")
    parser.add_argument("--host", default="127.0.0.1", help="Host IP address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8080, help="Port number (default: 8080).")
    return parser.parse_args()


def send_file(conn: socket.socket, file_path: str) -> None:
    """Отправляет файл по сокету."""
    file_size = os.path.getsize(file_path)
    conn.sendall(str(file_size).encode().ljust(16))
    with open(file_path, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            conn.sendall(bytes_read)


def handle_client(conn: socket.socket, addr: Tuple[str, int], file_path: str) -> None:
    """Обрабатывает подключение клиента."""
    print(f"request from {addr[0]}:{addr[1]}")
    print("sending...")
    send_file(conn, file_path)
    print(f"finished sending to {addr[0]}:{addr[1]}")
    conn.close()


def main() -> None:
    """Основная функция сервера."""
    args = parse_args()
    host = args.host
    port = args.port
    file_path = args.file_path

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"serving {file_path}")
            while True:
                conn, addr = s.accept()
                with conn:
                    handle_client(conn, addr, file_path)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
