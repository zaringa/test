import socket
import argparse
import os
from typing import Tuple

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UDP Client for file download.")
    parser.add_argument("output_file", help="Path to save the downloaded file.")
    parser.add_argument("--host", default="127.0.0.1", help="Server IP address.")
    parser.add_argument("--port", type=int, default=8080, help="Port number.")
    return parser.parse_args()

def receive_file(sock: socket.socket, server_addr: Tuple[str, int], output_file: str) -> None:
    with open(output_file, "wb") as f:
        while True:
            data, _ = sock.recvfrom(4096)
            if not data:
                break
            if data == b"END":
                break
            f.write(data)
    print(f"downloaded as {output_file}")

def main() -> None:
    args = parse_args()
    host = args.host
    port = args.port
    output_file = args.output_file

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            server_addr = (host, port)
            sock.sendto(b"RQST", server_addr)
            receive_file(sock, server_addr, output_file)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
