import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory # 獲取功能包share目錄絕對路徑
import os

def main():
    #   獲取圖片的真實路徑
    default_image_path = os.path.join(get_package_share_directory('demo_python_service'),'resource/default.jpg')
    print(f"圖片的真實路徑:{default_image_path}")
    #   使用cv2來加載圖片
    image = cv2.imread(default_image_path)
    #   檢測人臉
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='hog')
    #   繪製人臉框
    for top,right,bottom,left in face_locations:
        cv2.rectangle(image,(left,top),(right,bottom),(255,0,0),4)
    #   結果顯示
    cv2.imshow('Face Detecte Result', image)
    cv2.waitKey(0)