#!/usr/bin/python
import socketserver
import json
from typing import List

clients = []


ROWS, COLS = 24, 40

def replace_substring_at_index(s: str, new_substring: str, index: int) -> str:
    return s[:index] + new_substring + s[index + len(new_substring):]


class TextEditorServer(socketserver.BaseRequestHandler):
    canvas: List[str] = ["." * COLS for _ in range(ROWS)]

    def handle(self):
        print(f"Client {self.client_address} connected.")

        # Add client to the list
        clients.append(self.request)

        # First connection: send the whole canvas
        first_message = {
            "type": "sync",
            "canvas": TextEditorServer.canvas
        }

        self.request.sendall(json.dumps(first_message).encode())

        try:
            while True:
                # Wait for any client to send us data
                data = self.request.recv(1024).decode()
                if not data:
                    print(f"Client {self.client_address} disconnected.")
                    break

                print(f"Received data:", data)

                # We expect from a client:
                # { "type": "update", "text": "...", "row": ..., "col": ..., "client_id": "...", "username": "..." }
                update = json.loads(data)

                if update["text"] == "\u000b":
                    print("received C-k so clearing the canvas")
                    TextEditorServer.canvas = ["." * COLS for _ in range(ROWS)]
                    update = {
                        "type": "sync",
                        "canvas": TextEditorServer.canvas
                    }
                    data = json.dumps(update)
                else:
                    TextEditorServer.canvas[update["row"]] = \
                        replace_substring_at_index(
                            TextEditorServer.canvas[update["row"]],
                            update["text"],
                            update["col"]
                        )

                # Broadcast received data to other clients
                print(f"broadcasting {update['type']}")
                data = json.dumps(update)
                for client in clients:
                    if update["type"] == "sync" or client != self.request:
                        client.sendall(data.encode())
                        print(f"Sent data to client")
        finally:
            clients.remove(self.request)
            print(f"Client {self.client_address} removed from active clients.")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    print(f"Starting server on {HOST}:{PORT}.")
    server = socketserver.ThreadingTCPServer((HOST, PORT), TextEditorServer)
    server.serve_forever()
