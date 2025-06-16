import rclpy
from rclpy.node import Node

def main():
    rclpy.init()    # 初始化工作，分配資源
    node = Node('python_node')  # 創建節點
    node.get_logger().info('你好 python 節點')    # 日誌訊息，info級別(ros2中日誌專用訊息)
    node.get_logger().warn('你好 python 節點')    # 日誌訊息，warn級別(ros2中日誌專用訊息)
    rclpy.spin(node)    # 運行節點，只要不主動退出或打斷他，不會主動停止
    rclpy.shutdown()    # 停止節點執行

if __name__ == '__main__':  # 確保運行為此main
    main()