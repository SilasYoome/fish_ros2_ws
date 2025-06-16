import rclpy
from rclpy.node import Node
from chapt4_interfaces.srv import FaceDetector

import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 獲取功能包share目錄絕對路徑
import os   # 真實路徑用
from cv_bridge import CvBridge  
import time

from rcl_interfaces.msg import SetParametersResult

class FaceDetectNode(Node):
    def __init__(self):
        super().__init__('face_detect_node')
        self.bridge = CvBridge()
        self.default_image_path = os.path.join(get_package_share_directory('demo_python_service'),'resource/default.jpg')
        self.get_logger().info("人臉檢測服務已經啟動")

        # 改寫為下方的參數聲明方法
        # self.number_of_times_to_upsample = 1
        # self.model = 'hog'
        # ===============參數聲明=================
        self.declare_parameter('number_of_times_to_upsample',1)
        self.declare_parameter('model','hog')
        self.number_of_times_to_upsample = self.get_parameter('number_of_times_to_upsample').value
        self.model = self.get_parameter('model').value
        # ===============參數聲明=================

        self.services_ = self.create_service(FaceDetector,'face_detect',self.detect_face_callback)

    # ===========若有參數變動並傳入，則進行更新===========
        self.add_on_set_parameters_callback(self.parameters_callback)

    def parameters_callback(self,parameters):
        for parameter in parameters:
            self.get_logger().info(f"{parameter.name}->{parameter.value}")
            if parameter.name == 'number_of_times_to_upsample':
                self.number_of_times_to_upsample = parameter.value
            if parameter.name == 'model':
                self.model = parameter.value
        return SetParametersResult(successful=True)
    # ===========若有參數變動並傳入，則進行更新===========


    def detect_face_callback(self, request, response):  # request:請求 response:響應
        if request.image.data:  #   判對是否有圖像傳入
            cv_image = self.bridge.imgmsg_to_cv2(request.image) #   將傳入的圖像格式轉為OpenCV可使用的格式
        else:
            cv_image = cv2.imread(self.default_image_path)  #   若判斷為沒有圖像傳入，則使用匯入預設路徑中的預設圖片
            self.get_logger().info(f"載入圖片為空，使用默認圖像。")

        #   cv_image已經是一個openCV的圖像了
        start_time = time.time()
        self.get_logger().info(f"加載完成圖像，開始識別。")
        #   檢測人臉
        face_locations = face_recognition.face_locations(cv_image, number_of_times_to_upsample=self.number_of_times_to_upsample, model=self.model)
        response.use_time = time.time() - start_time
        response.number = len(face_locations)
        for top,right,bottom,left in face_locations:
            response.top.append(top)
            response.right.append(right)
            response.bottom.append(bottom)
            response.left.append(left)

        return response #   必須返回response

def main(args=None):
    rclpy.init(args=args)
    node = FaceDetectNode()
    rclpy.spin(node)
    rclpy.shutdown()
