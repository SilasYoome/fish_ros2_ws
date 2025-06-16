import rclpy
from status_interfaces.msg import SystemStatus  # 導入消息接口
from rclpy.node import Node
import psutil       # 獲取系統訊息
import platform     # 獲取主機名字

class SysStatusPub(Node):
    def __init__(self, node_name):
        self.status_publisher_ = self.create_publisher(
                SystemStatus, 'sys_tatus', 10
        )
        self.timers_ = self.create_timer(1.0,self.timer_callback)

    def timer_callback(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        net_io_counters = psutil.net_io_counters()

        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total /1024/1024
        msg.memory_availabel = memory_info.available /1024/1024
        msg.net_sent = net_io_counters.bytes_sent /1024/1024
        msg.net_recv = net_io_counters.bytes_recv /1024/1024

        self.get_logger().info(f'发布:{str(msg)}')
        self.status_publisher_.publish(msg)

def main():
    rclpy.init()
    node = SystemStatus("sys_status_pub")
    rclpy.spin(node)
    rclpy.shutdown()