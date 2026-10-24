import io, os

ITEMS = [
    ("docs/hardware/linux/systemd.mdx", "## 依赖与顺序：两件不同的事",
     "linux-systemd-dep.svg",
     "systemd 依赖关系：After 只管顺序，Requires 管依赖；只写 Requires 不写 After 会导致两个服务同时启动"),
    ("docs/hardware/linux/tools-disk.mdx", "## 分区表：MBR 与 GPT",
     "linux-partition-tables.svg",
     "MBR 与 GPT 分区表布局对比：MBR 上限 2TiB 最多 4 主分区，GPT 有备份表与 CRC 且支持 128 分区"),
    ("docs/hardware/esp-basics/36-ble.mdx", "## GATT：数据的组织方式",
     "esp32-ble-gatt.svg",
     "BLE 的 GATT 四层结构 Profile/Service/Characteristic/Descriptor，以及心率传感器的实际例子"),
    ("docs/chips/stm32/watchdog.mdx", "## WWDG：窗口机制",
     "stm32-wwdg-window.svg",
     "WWDG 窗口看门狗时序：计数值从 0x7F 递减，只有在 0x50 到 0x40 之间喂狗才算数，喂早喂晚都复位"),
    ("docs/chips/stm32/freertos-sync.mdx", "## 六种机制速查",
     "stm32-freertos-sync.svg",
     "FreeRTOS 六种同步原语按解决的问题分类：队列传数据、信号量通知、互斥锁独占、事件组等多个条件、任务通知最快"),
    ("docs/software/c/concurrency.mdx", "## 数据竞争：最隐蔽的 bug",
     "c-data-race.svg",
     "数据竞争时序：线程 A 和 B 都读到旧值 5，各自加 1 写回 6，两次自增只生效一次"),
]

ok = 0
for path, anchor, img, alt in ITEMS:
    if not os.path.exists(path):
        print("MISSING", path); continue
    lines = io.open(path, encoding="utf-8").read().split(chr(10))
    idx = None
    for i, l in enumerate(lines):
        if l.strip() == anchor.strip():
            idx = i; break
    if idx is None:
        print("ANCHOR MISS", path, "|", anchor); continue
    if img in chr(10).join(lines):
        print("EXISTS", path); continue
    lines[idx+1:idx+1] = ["", "![%s](/img/diagrams/%s)" % (alt, img), ""]
    io.open(path, "w", encoding="utf-8", newline=chr(10)).write(chr(10).join(lines))
    print("OK", path); ok += 1
print("inserted", ok, "/", len(ITEMS))