import http.server
import socketserver

PORT = 8001


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="date", **kwargs)


def porneste_serverul():
    with socketserver.TCPServer(("", PORT), Handler) as server:
        print("Datele sunt pe http://127.0.0.1:" + str(PORT) + "/jucatori.json")
        server.serve_forever()


if __name__ == "__main__":
    porneste_serverul()
