---
type: note
status: seed
topic:
difficulty: 1
created: 2026-11-07
review_at:
verified: false
last_verified:
tags:
  - devops
---

# Namespaces 
## Зачем это нужно

Namespaces - нужны для того, чтобы ограничивать ресурсы и процессы друг от друга, чтобы один процесс мог запускать что-либо не видя другой.
## Ключевая идея

Самый новый - это time namespace (since 5.6), он позволяет контролировать временной namespace процесса (понятия не имею что это за зверь)

     Namespace   Flag              Page                    Isolates
     ─────────────────────────────────────────────────────────────────────────────────
     Cgroup      CLONE_NEWCGROUP   cgroup_namespaces(7)    Cgroup root directory
     IPC         CLONE_NEWIPC      ipc_namespaces(7)       System V IPC, POSIX message queues
     Network     CLONE_NEWNET      network_namespaces(7)   Network devices, stacks, ports, etc.
     Mount       CLONE_NEWNS       mount_namespaces(7)     Mount points
     PID         CLONE_NEWPID      pid_namespaces(7)       Process IDs
     Time        CLONE_NEWTIME     time_namespaces(7)      Boot and monotonic clocks
     User        CLONE_NEWUSER     user_namespaces(7)      User and group IDs
     UTS         CLONE_NEWUTS      uts_namespaces(7)       Hostname and NIS domain name
## Как работает

1. Ну мне видны mnt, net, time, cgroup, pid, user, uts, ipc (ну тоесть все), bash process - 133546, 
readlink /proc/\$\$/ns/pid /proc/\$\$/ns/net /proc/\$\$/ns/mnt
'pid:[4026531836]'
'net:[4026531833]'
'mnt:[4026531832]'
348 - процессов.
2.л 
- pid 1! потому как я зарегистровал его как корневой используя флаг --map-root-user, тоесть этот процесс считается корневым. 
- Здесь только 2 процесса, видит он только bash и запущенный ps aux
- Разная группа процессов, 'pid:[4026532710]'
- Без fork, процесс не создался бы вовсе 
unshare: mount /proc failed: Operation not permitted
а без mount-proc оно запустится, но он не будет примонтирован к своей группе, все процессы будут видны, но он будет помечен как корневой процесс в echo \$\$
3. 354, при этом других процессов я не запускал 
4. Изнутри чужого неймспейса видно только то, что может быть видно в самом неймспейсе, полезно для захода внутрь контейнера к примеру командой docker exec -it bash. Опасно тем, что из namespace можно сбежать, а также тем, что если завершить процесс 1 в неймспейсе упадет весь неймспейс ( If the "init" process of a PID namespace terminates, the kernel terminates all of the  processes  in the  namespace via a SIGKILL signal.  This behavior reflects the fact that the "init" process is essential for the correct operation of a PID namespace.)
 
## Ошибки и подводные камни
 sysctl kernel.unprivileged_userns_clone 2>/dev/null; cat /proc/sys/user/max_user_namespaces
kernel.unprivileged_userns_clone = 1
─────┬──────────────────────────────────────────────────────────────────
     │ File: /proc/sys/user/max_user_namespaces
─────┼──────────────────────────────────────────────────────────────────
   1 │ 63073
─────┴──────────────────────────────────────────────────────────────────

## Проверка себя

## Связи

> [!check] Проверено
> - Дата:
> - Окружение:
> - Источники:
> - Проверенные команды:
> - Не проверено:
