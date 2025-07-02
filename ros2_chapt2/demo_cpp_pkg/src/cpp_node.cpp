#include "rclcpp/rclcpp.hpp"   // 寫C頭文件習慣為.h 寫C++時頭文件習慣為.hpp

int main(int argc, char** argv)
{
    rclcpp::init(argc,argv);    // 初始化 傳遞argc,argv的用意在於，讓使用者可以使用ros2的其他修改指令，比如說修改node節點
    /* 節點(node)可以使用auto(自動類型推導)來宣告 */
    auto node = std::make_shared<rclcpp::Node>("cpp_node"); 
    RCLCPP_INFO(node->get_logger(),"你好C++節點");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}