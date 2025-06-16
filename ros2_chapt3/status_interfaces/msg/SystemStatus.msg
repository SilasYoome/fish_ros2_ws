builtin_interfaces/Time stamp # 時間戳   ros2 interface list | grep Time 指令來尋找，會獲取builtin_interfaces/msg/Time，使用時要把msg去掉
string host_name # 主機名字
float32 cpu_percent # CPU使用率
float32 memory_percent # 記憶體使用率
float32 memory_total # 記憶體組大小
float32 memory_availabel # 記憶剩餘大小
float64 net_sent # 網路發送數據總量 1MB=8Mb
float64 net_recv # 網路數據接受總量 MB