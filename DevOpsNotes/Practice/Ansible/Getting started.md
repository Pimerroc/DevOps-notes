Установил ansible и создал директорию по документации
```bash
pip install ansible
mkdir ansible_quickstart && cd ansible_quickstart
```
Потом создать виртуалку и вставить ее ip в последствии
(port forwarding localhost:22222 server_ip:22)
```text title=inventory.ini
[myhosts]
127.0.0.1 ansible_host=127.0.0.1 ansible_port=22222 ansible_user=mex
```
Но конечно же за место того, чтобы писать какие-то ini для маленьких систем будет считать что система у нас болшая, следовательно нам необходимо писать yamlики;
```yaml title=inventory.yaml
myhosts:
  hosts:
    localhost:
      ansible_host: 127.0.0.1
      ansible_user: mex
      ansible_port: 22222
```
Далее написал playbook.yaml который выводит сообщение Hello world от каждой ноды:
```yaml tiltle=playbook.yaml
- name: My first play
  hosts: myhosts
  tasks:
    - name: Ping my hosts
      ansible.builtin.ping:
    - name: Print message
      ansible.builtin.debug:
        msg: Hello world

```
# [[Ansible concepts|Терминология]]

