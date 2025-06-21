import socket
import argparse
import os
from typing import Tuple

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="UDP Server for file transfer.")
    parser.add_argument("file_path", help="Path to the file to serve.")
    parser.add_argument("--host", default="127.0.0.1", help="Host IP address (default: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=8080, help="Port number (default: 8080).")
    return parser.parse_args()


def send_file(sock: socket.socket, addr: Tuple[str, int], file_path: str) -> None:
    """Отправляет файл по UDP."""
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            sock.sendto(bytes_read, addr)


def main() -> None:
    """Основная функция UDP сервера."""
    args = parse_args()
    host = args.host
    port = args.port
    file_path = args.file_path

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((host, port))
            print(f"serving {file_path}")

            while True: 
                data, addr = sock.recvfrom(1024)
                if data == b"RQST":
                    print(f"request from {addr[0]}:{addr[1]}")
                    print("sending...")
                    send_file(sock, addr, file_path)
                    print(f"finished sending to {addr[0]}:{addr[1]}")
                    break  
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
