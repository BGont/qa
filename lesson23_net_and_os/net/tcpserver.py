import socket

HTML_TEMPLATE = '''<html>
<head>
    <title>Простой блокирующий tcp-сервер</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Заголовки запроса:</h1>
    {payload}
</body>
</html>'''

HEADER_TEMPLATE = "<div><strong>{header_name}:</strong> {header_value}</div>\n"


def extract_headers(request):
    headers = []
    request_parts = request.split(sep="\r\n")[1:]
    for row in request_parts:
        if row == '':
            break
        header_name, header_value = row.split(sep=": ", maxsplit=1)
        if header_name == "Cookie":
            continue
        headers.append((header_name, header_value))

    return headers


def response_html(request):
    headers = extract_headers(request)
    payload = ''
    for header_struct in headers:
        header_name, header_value = header_struct
        payload += HEADER_TEMPLATE.format(header_name=header_name, header_value=header_value)

    return HTML_TEMPLATE.format(payload=payload)


def server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        while True:
            new_socket, address = sock.accept()
            while True:
                received_data = new_socket.recv(2048).decode("utf-8")
                if not received_data:
                    break
                http_payload = f"{response_html(received_data)}\r\n".encode("utf-8")
                content_length = len(http_payload)
                new_socket.send("HTTP/1.1 200 OK\r\n"
                                "Connection: close\r\n"
                                "Content-Type: text/html\r\n"
                                f"Content-Length: {content_length}\r\n"
                                "\r\n".encode("utf-8") + http_payload
                                )


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8001

    server(HOST, PORT)
