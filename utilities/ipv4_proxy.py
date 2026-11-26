"""Local CONNECT/HTTP proxy that resolves origin hosts to IPv4 only.

Workaround for this line's black-holed Cloudflare IPv6 (SYNs never complete).
Point HTTPS_PROXY / HTTP_PROXY at http://127.0.0.1:8888 for the download process tree.
Plain byte pipe for tunnels; A-records-only resolution (AF_INET) for origins.
"""
import socket
import threading

HOST, PORT = "127.0.0.1", 8888


def pipe(a, b):
    try:
        while True:
            d = a.recv(65536)
            if not d:
                break
            b.sendall(d)
    except OSError:
        pass
    for s in (b, a):
        try:
            s.shutdown(socket.SHUT_WR)
        except OSError:
            pass


def resolve_ipv4(host, port):
    infos = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
    if not infos:
        return None
    return (infos[0][4][0], port)


def handle(conn):
    try:
        req = b""
        while b"\r\n\r\n" not in req:
            chunk = conn.recv(8192)
            if not chunk:
                return
            req += chunk
        head = req.split(b"\r\n", 1)[0].decode(errors="ignore")
        method, _, rest = head.partition(" ")
        if method.upper() == "CONNECT":
            hostport = rest.split()[0] if rest else ""
            host, _, port = hostport.partition(":")
            addr = resolve_ipv4(host, int(port or 443))
            if addr is None:
                conn.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                return
            upstream = socket.create_connection(addr, timeout=60)
            conn.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            print(f"CONNECT {host}:{addr[1]} -> {addr[0]}", flush=True)
            # ONE reader per direction: thread pipes upstream->conn, main pipes conn->upstream
            t = threading.Thread(target=pipe, args=(upstream, conn), daemon=True)
            t.start()
            pipe(conn, upstream)
            t.join()
        elif method.upper() in ("GET", "HEAD"):
            url = rest.split()[0]
            if url.startswith("http://"):
                from urllib.parse import urlparse
                p = urlparse(url)
                addr = resolve_ipv4(p.hostname, p.port or 80)
                if addr is None:
                    conn.sendall(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
                    return
                path = p.path + ("?" + p.query if p.query else "")
                upstream = socket.create_connection(addr, timeout=60)
                # rewrite the request line to origin-form
                new_head = f"GET {path} HTTP/1.1\r\n"
                headers = req.split(b"\r\n\r\n", 1)[0].decode(errors="ignore").split("\r\n")[1:]
                headers = [h for h in headers if not h.lower().startswith("host:")]
                headers.append(f"Host: {p.hostname}")
                upstream.sendall((new_head + "\r\n".join(headers) + "\r\n\r\n").encode())
                print(f"{method} {host}:{addr[1]}", flush=True)
                t = threading.Thread(target=pipe, args=(upstream, conn), daemon=True)
                t.start()
                pipe(conn, upstream)
                t.join()
            else:
                conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
        else:
            conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
    except Exception:
        pass
    finally:
        try:
            conn.close()
        except OSError:
            pass


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(64)
    print(f"ipv4-only proxy listening on {HOST}:{PORT}", flush=True)
    while True:
        c, _ = s.accept()
        threading.Thread(target=handle, args=(c,), daemon=True).start()


if __name__ == "__main__":
    main()
