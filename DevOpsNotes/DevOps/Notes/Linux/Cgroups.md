---
type: note
status: seed
topic:
difficulty: 1
created: "{{date:YYYY-MM-DD}}"
review_at:
verified: false
last_verified:
tags: [devops]
---

# Cgroups 

> [!summary] Одно предложение: зачем это нужно и где применяется.

## Зачем это нужно

Необходимо для ограничения потребления ресурсов, некоторой группы процессов или неймспейса. Применяется для контейнеризации.
## Ключевая идея
Ограничить ресурсы процессов, чтобы они не могли выходить за их пределы. Например если нам надо ограничить число ядер задействованных для выполнения той или иной задачи, или же объем задействованной памяти. 
## Как работает

## Практика

Просто посмотреть на группу с небольшими ограничениями, но вообще можно внутри слайса создавать группу (к примеру внутри /sys/fs/cgroup/user.slice/user-1000.slice/ )
Внизу представлен примитивный пример создания, после будет уже сама лабаI.
```text
❯ cat /proc/self/cgroup
─────┬─────────────────────────────────────────────────────────────────
     │ File: /proc/self/cgroup
─────┼─────────────────────────────────────────────────────────────────
   1 │ 0::/user.slice/user-1000.slice/user@1000.service/app.slice/kitty
     │ -34390-0.scope
─────┴─────────────────────────────────────────────────────────────────
❯ cd /sys/fs/cgroup/user.slice/user-1000.slice
❯ ls
cgroup.controllers      cpu.stat.local       memory.reclaim
cgroup.events           cpu.uclamp.max       memory.stat
cgroup.freeze           cpu.uclamp.min       memory.swap.current
cgroup.kill             cpu.weight           memory.swap.events
cgroup.max.depth        cpu.weight.nice      memory.swap.high
cgroup.max.descendants  io.pressure          memory.swap.max
cgroup.pressure         irq.pressure         memory.swap.peak
cgroup.procs            memory.current       memory.zswap.current
cgroup.stat             memory.events        memory.zswap.max
cgroup.stat.local       memory.events.local  memory.zswap.writeback
cgroup.subtree_control  memory.high          pids.current
cgroup.threads          memory.low           pids.events
cgroup.type             memory.max           pids.events.local
cpu.idle                memory.min           pids.max
cpu.max                 memory.numa_stat     pids.peak
cpu.max.burst           memory.oom.group     session-3.scope
cpu.pressure            memory.peak          user@1000.service
cpu.stat                memory.pressure
❯ sudo mkdir supergroup
❯ cd supergroup
❯ ls
cgroup.controllers      cpu.stat             memory.peak
cgroup.events           cpu.stat.local       memory.pressure
cgroup.freeze           cpu.uclamp.max       memory.reclaim
cgroup.kill             cpu.uclamp.min       memory.stat
cgroup.max.depth        cpu.weight           memory.swap.current
cgroup.max.descendants  cpu.weight.nice      memory.swap.events
cgroup.pressure         io.pressure          memory.swap.high
cgroup.procs            irq.pressure         memory.swap.max
cgroup.stat             memory.current       memory.swap.peak
cgroup.stat.local       memory.events        memory.zswap.current
cgroup.subtree_control  memory.events.local  memory.zswap.max
cgroup.threads          memory.high          memory.zswap.writeback
cgroup.type             memory.low           pids.current
cpu.idle                memory.max           pids.events
cpu.max                 memory.min           pids.events.local
cpu.max.burst           memory.numa_stat     pids.max
cpu.pressure            memory.oom.group     pids.peak
```

```bash
sudo systemd-run --unit=cgtest --collect \
  --property=MemoryMax=50M --property=CPUQuota=20% \
  stress-ng --cpu 2 --vm 1 --vm-bytes 30M --timeout 300s
```

```bash
❯ ls /sys/fs/cgroup/system.slice/cgtest.service/
cgroup.controllers      cpu.pressure                     io.max               memory.pressure
cgroup.events           cpuset.cpus                      io.pressure          memory.reclaim
cgroup.freeze           cpuset.cpus.effective            io.prio.class        memory.stat
cgroup.kill             cpuset.cpus.exclusive            io.stat              memory.swap.current
cgroup.max.depth        cpuset.cpus.exclusive.effective  io.weight            memory.swap.events
cgroup.max.descendants  cpuset.cpus.partition            irq.pressure         memory.swap.high
cgroup.pressure         cpuset.mems                      memory.current       memory.swap.max
cgroup.procs            cpuset.mems.effective            memory.events        memory.swap.peak
cgroup.stat             cpu.stat                         memory.events.local  memory.zswap.current
cgroup.stat.local       cpu.stat.local                   memory.high          memory.zswap.max
cgroup.subtree_control  cpu.uclamp.max                   memory.low           memory.zswap.writeback
cgroup.threads          cpu.uclamp.min                   memory.max           pids.current
cgroup.type             cpu.weight                       memory.min           pids.events
cpu.idle                cpu.weight.nice                  memory.numa_stat     pids.events.local
cpu.max                 io.bfq.weight                    memory.oom.group     pids.max
cpu.max.burst           io.latency                       memory.peak          pids.peak
❯ cat /sys/fs/cgroup/system.slice/cgtest.service/memory.max
─────┬─────────────────────────────────────────────────────────────────────────
     │ File: /sys/fs/cgroup/system.slice/cgtest.service/memory.max
─────┼──────────────────────────────────────────────────────────────────────────
   1 │ 52428800
─────┴───────────────────────────────────────────────────────────────────────────
❯ 
❯ cat /sys/fs/cgroup/system.slice/cgtest.service/cpu.max
─────┬───────────────────────────────────────────────────────────────────────────
     │ File: /sys/fs/cgroup/system.slice/cgtest.service/cpu.max
─────┼───────────────────────────────────────────────────────────────────────────
   1 │ 20000 100000
─────┴───────────────────────────────────────────────────────────────────────────
CGroup                          Tasks   %CPU   Memory  Input/s Output/s
/                                1648   21.9     5.8G       0B    23.8K
user.slice                       1337   20.0    12.6G       0B    23.8K
user.slice/user-1000.slice       1337   19.9    12.1G        -        -
user.slic…e/user@1000.service    1327   19.9    12.1G        -        -
system.slice                       85    0.2   438.9M        -        -
system.slice/upower.service         4    0.1     4.7M        -        -
system.sl…/containerd.service      17    0.1   100.6M        -        -
system.sl…dbus-broker.service       2    0.0     5.5M        -        -
system.sl…e/bluetooth.service       1    0.0     4.1M        -        -
system.sl…md-journald.service       1    0.0    76.9M        -        -
system.slice/udisks2.service        7    0.0     6.7M        -        -
dev-hugepages.mount                 -      -     340K        -        -
dev-mqueue.mount                    -      -     460K        -        -
init.scope                          1      -     7.1M        -        -
proc-sys-fs-binfmt_misc.mount       -      -      12K        -        -
sys-fs-fuse-connections.mount       -      -       8K        -        -
sys-kernel-config.mount             -      -       4K        -        -
sys-kernel-debug.mount              -      -     400K        -        -
sys-kernel-tracing.mount            -      -      96K        -        -
system.sl…workManager.service       4      -    21.3M        -        -
system.sl…unts-daemon.service       4      -     1.9M        -        -
system.slice/boot.mount             -      -      28K        -        -
system.slice/colord.service         4      -    26.5M        -        -
system.slice/dev-zram0.swap         -      -     224K        -        -
system.slice/docker.service        20      -   130.2M        -        -
system.slice/gdm.service            5      -     5.3M        -        -
system.slice/home.mount             -      -       8K        -        -
system.slice/polkit.service         4      -     5.6M        -        -
system.sl…tkit-daemon.service       3      -     672K        -        -
system.sl…zram\x2dsetup.slice       -      -      92K        -        -
system.sl…temd-logind.service       1      -     2.4M        -        -
system.sl…d-timesyncd.service       2      -     2.3M        -        -
system.sl…stemd-udevd.service       1      -    19.2M        -        -
system.sl…emd-userdbd.service       4      -       4M        -        -
system.slice/tmp.mount              -      -      12K        -        -
system.sl…he-pacman-pkg.mount       -      -      16K        -        -
system.slice/var-log.mount          -      -      12K        -        -
system.sl…_supplicant.service       1      -     6.1M        -        -
user.slic…ice/session-3.scope      10      -     3.8M        -        -
```

Условные лимиты (тротлинг)
```bash
❯ sudo systemd-run --unit=cghigh --collect \
  --property=MemoryHigh=30M --property=MemoryMax=50M \
  stress-ng --vm 1 --vm-bytes 100M --timeout 60s
Running as unit: cghigh.service; invocation ID: 68e6532295e94dcab61d160f4bda1690
❯ systemctl status cghigh
● cghigh.service - [systemd-run] /usr/bin/stress-ng --vm 1 --vm-bytes >
     Loaded: loaded (/run/systemd/transient/cghigh.service; transient)
  Transient: yes
     Active: active (running) since Sat 2026-11-14 18:03:17 MSK; 51s a>
 Invocation: 686a3a38835544e38f1a7c29a7c5b6e3
   Main PID: 35442 (stress-ng)
      Tasks: 3 (limit: 18921)
     Memory: 31M (high: 30M, max: 50M, available: 0B, peak: 49.5M, swa>
        CPU: 50.801s
     CGroup: /system.slice/cghigh.service
             ├─35442 /usr/bin/stress-ng --vm 1 --vm-bytes 100M --timeo>
             ├─35450 stress-ng-vm "" "" "" "" "" .
             └─35451 stress-ng-vm "" "" "" "" "" .

Nov 14 18:03:17 Pimerroc systemd[1]: Started [systemd-run] /usr/bin/st>
Nov 14 18:03:17 Pimerroc stress-ng[35442]: invoked with '/usr/bin/stre>
Nov 14 18:03:17 Pimerroc stress-ng[35442]: system: 'Pimerroc' Linux 7.>
Nov 14 18:03:17 Pimerroc stress-ng[35442]: stress-ng: info:  [35442] s>
Nov 14 18:03:17 Pimerroc stress-ng[35442]: memory (MB): total 15822.29>
Nov 14 18:03:17 Pimerroc stress-ng[35442]: stress-ng: info:  [35442] d>
Nov 14 18:03:17 Pimerroc stress-ng[35450]: stress-ng: info:  [35450] v>
❯ cat /sys/fs/cgroup/system.slice/cghigh.service/memory.events
─────┬─────────────────────────────────────────────────────────────────
     │ File: /sys/fs/cgroup/system.slice/cghigh.service/memory.even
     │ ts
─────┼─────────────────────────────────────────────────────────────────
   1 │ low 0
   2 │ high 35172
   3 │ max 5
   4 │ oom 0
   5 │ oom_kill 0
   6 │ oom_group_kill 0
   7 │ sock_throttled 0
─────┴─────────────────────────────────────────────────────────────────
```

Жесткие лимиты
```bash
❯ sudo systemd-run --unit=cgoom --collect \
  --property=MemoryMax=50M --property=MemorySwapMax=0 \
  stress-ng --vm 1 --vm-bytes 200M --timeout 60s
Running as unit: cgoom.service; invocation ID: a985a5499a734affb41cf240d9b5a868
❯ systemctl status cgoom
Unit cgoom.service could not be found.
❯ journalctl -r | head -n 400 | grep -i "OOM"
Pimerroc systemd[1]: cgoom.service: Failed with result 'oom-kill'.
❯ journalctl -u cgoom | tail -n 20
Pimerroc systemd[1]: Started [systemd-run] /usr/bin/stress-ng --vm 1 --vm-bytes 200M --timeout 60s.
Pimerroc stress-ng[39601]: invoked with '/usr/bin/stress-ng --vm 1 --vm-bytes 200M --timeout 60s' by user 0 'root'
Pimerroc stress-ng[39601]: system: 'Pimerroc' Linux 7.3.4-arch1-1 #1 SMP PREEMPT_DYNAMIC Wed, 11 Nov 2026 19:02:39 +0000 x86_64
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] setting to a 1 min run per stressor
Pimerroc stress-ng[39601]: memory (MB): total 15822.29, free 617.88, shared 179.20, buffer 2.57, swap 4096.00, free swap 4096.00
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] dispatching hogs: 1 vm
Pimerroc stress-ng[39605]: stress-ng: info:  [39605] vm: using 200MB per stressor instance (total 200MB of 617.87MB available memory)
Pimerroc systemd[1]: cgoom.service: The kernel OOM killer killed some processes in this unit.
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] stopping 1 stressors
Pimerroc stress-ng[39605]: memory (MB): total 15822.29, free 622.84, shared 179.39, buffer 2.57, swap 4096.00, free swap 4096.00
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] skipped: 0
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] passed: 1: vm (1)
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] failed: 0
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] metrics untrustworthy: 0
Pimerroc stress-ng[39601]: stress-ng: info:  [39601] successful run completed in 0 secs
Pimerroc systemd[1]: cgoom.service: Failed with result 'oom-kill'.
❯ cat /sys/fs/cgroup/system.slice/cgoom.service/memory.events 2>/dev/null || echo "дир уже исчезла"
дир уже исчезла
```
Тоесть наша группа при создании появилась, и тут же умерла.
## Ошибки и подводные камни

## Проверка себя

## Связи

> [!check] Проверено
> - Дата:
> - Окружение:
> - Источники:
> - Проверенные команды:
> - Не проверено:
