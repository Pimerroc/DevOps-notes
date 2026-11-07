![[Pasted image 20260916200517.png]]

1. Попросил гпт написать простой HTTP сервер и закинул его на хост
```python
from http.server import HTTPServer, BaseHTTPRequestHandler


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Hello, world!\n"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)


server = HTTPServer(("0.0.0.0", 8080), Handler)

print("Listening on port 8080...")
server.serve_forever()
```
 2. vim /etc/systemd/system/simpleServerHandler.service
 для понимания можно просмотреть `systemd.unit(5)`
```service
[Unit]
Description=Simple server restarting unit

[Service]
Type=simple
ExecStart=python /home/max/server.py
Restart=on-failure
RestartSec=2
```
3. далее просто запустить его с помощью systemctl
4. systemctl enable --now simpleServerHandler.service
5. systemctl status simpleServerHandler.service в нем посмотреть где расположена cgroup (обычно `/sys/fs/cgroup/system.slice/myservice/`)
6. Далее меняем файл memory.max вводя к примеру 50M
(они сами потом поменяются под определенное число МБ)
Чтобы даже после kill -9 было такое же значение необходимо в 
сервисе указать:
```text
[Service]
MemoryMax=(max, 5G etc)
```
