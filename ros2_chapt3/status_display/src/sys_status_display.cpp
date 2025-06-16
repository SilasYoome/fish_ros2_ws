#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SysStatusDisplay : public rclcpp::Node
{
private:
    /* data */
    //  創建訂閱者，用來訂閱python編寫的發布者的內容
    rclcpp::Subscription<SystemStatus>::SharedPtr subscription_;

    //  QT初始化
    QLabel *label_;
public:
    SysStatusDisplay(/* args */):Node("sys_status_display")
    {
        subscription_ = this->create_subscription<SystemStatus>(
            "sys_tatus", 10, [&](const SystemStatus::SharedPtr msg) -> void {
              label_->setText(get_qstr_from_msg(msg));
            }); 
        label_ = new QLabel(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label_->show();
    };

    //  將訂閱者獲取的資訊msg放入QT的成員setText中
    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str << 
        "==========系統狀態可視化顯示工具==========\n" <<
        "數 據 時 間：\t"<< msg->stamp.sec << "\ts\n" <<
        "主 機 名 字：\t"<< msg->host_name << "\t\n" <<
        "CPU 使用率 ：\t"<< msg->cpu_percent << "\t%\n" <<
        "RAM 使用率 ：\t"<< msg->memory_percent << "\t%\n" <<
        "RAM 總大小 ：\t"<< msg->memory_total << "\tMB\n" <<
        "RAM剩餘可用大小：\t"<< msg->memory_availabel << "\tMB\n" <<
        "網路發送量：\t"<< msg->net_sent << "\tMB\n" <<
        "網路接收量：\t"<< msg->net_recv << "\tMB\n" <<
        "========================================";
        return QString::fromStdString(show_str.str());
    }
};




int main(int argc, char* argv[]) {
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SysStatusDisplay>();
    std::thread spin_thread([&]() -> void { rclcpp::spin(node); });
    spin_thread.detach();
    app.exec();
    rclcpp::shutdown();
    return 0;
}