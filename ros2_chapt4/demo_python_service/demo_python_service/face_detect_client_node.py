import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 獲取功能包share目錄絕對路徑
import os   # 真實路徑用
from cv_bridge import CvBridge  
import time

class FaceDetectNodeClient(Node):
    def __init__(self):
        super().__init__('face_detect_client_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'),'resource/test1.jpg')
        self.get_logger().info("人臉檢測客戶端已經啟動")
        self.client = self.create_client(FaceDetector,'face_detect')
        self.image = cv2.imread(self.default_image_path)

    # 發送請求給服務端
    def send_request(self):
        # 1.判斷服務端是否在線
        while self.client.wait_for_service(timeout_sec=1.0) is False:
            self.get_logger().info('等待服務端上線')
        # 2.建立request
        request = FaceDetector.Request()
        request.image = self.bridge.cv2_to_imgmsg(self.image)
        # 3.發送請求並等待處理完成
        future = self.client.call_async(request) # 現在的future並沒有包含回應結果，需要等待服務端處裡完成才會把結果放到future中

        # while future.done():
        # 休眠當前執行程式，等待服務處裡完成，造成當前程式無法再接收來自服務端的返回，導致永選沒有辦法完成=> future.done無法返回True
            # time.sleep(1.0) 


        # rclpy.spin_until_future_complete(self,future)
        # response = future.result()  # 獲取回應
        # self.get_logger().info(f'接收回應，共有{response.number}張人臉，耗時{response.use_time}s')
        # self.show_response(response)

        def result_callback(result_future):
            response = future.result()  # 獲取回應
            self.get_logger().info(f'接收回應，共有{response.number}張人臉，耗時{response.use_time}s')
            self.show_response(response)
        future.add_done_callback(result_callback)   # ros自帶，收到服務端完成消息後執行callback函數

    # 對回傳結果處裡
    def show_response(self,response):
        for i in range(response.number):
            top = response.top[i]
            right = response.right[i]
            bottom = response.bottom[i]
            left = response.left[i]
            cv2.rectangle(self.image,(left,top),(right,bottom),(255,0,0),4)
        cv2.imshow('Face Detecte Result', self.image)
        cv2.waitKey(0)  # waitkey也會阻塞程式，會導致spin無法正常運行


def main(args=None):
    rclpy.init(args=args)
    node = FaceDetectNodeClient()
    node.send_request()
    rclpy.spin(node)
    rclpy.shutdown()
