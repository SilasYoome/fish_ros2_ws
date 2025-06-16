import rclpy
from rclpy.node import Node

class PersonMode(Node):
    # python class方法中的第一個函數，規定一定為self
    def __init__(self ,node_name:str,name_value:str, age_value: int) -> None:
        print('PersonNode __init__方法被調用了，添加了兩個屬性')
        super().__init__(node_name)
        self.name = name_value
        self.age = age_value
    
    def eat(self,food_name:str):
        """
        方法：吃東西
        :food_name 食物名字
        """
        # print(f"{self.name},{self.age}歲，愛吃{food_name}")
        self.get_logger().info(f"{self.name},{self.age}歲，愛吃{food_name}")


def main():
    rclpy.init()
    node = PersonMode('person_node','超級英雄大哥',18)
    node.eat('青椒炒肉絲')
    rclpy.spin(node)
    rclpy.shutdown()