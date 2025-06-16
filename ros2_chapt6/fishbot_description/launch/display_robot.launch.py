import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory # 尋找目錄用
import os

import launch_ros.parameter_descriptions

def generate_launch_description():
    # 獲取默認的urdf路徑
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_urdf_path = os.path.join(urdf_package_path,'urdf','first_robot.urdf')
    default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')

    # 聲明一個urdf目錄的參數，方便修改
    # launch.actions.DeclareLaunchArgument用於聲明一個啟動參數
    action_declate_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model',                           # 參數名稱
        default_value=str(default_urdf_path),   # 預設值(可選)
        description='加載的模型文件路徑'            # 參數描述(可選)
    )



    # 通過文件路徑，獲取內容，並轉換成參數值對象，以供傳入robot_state_publisher
    
    # 如果要啟動urdf文件，要使用cat指令
    # substitutions_command_result = launch.substitutions.Command(['cat ',launch.substitutions.LaunchConfiguration('model')])   # 讓launch執行shell指令，並在後方接上urdf檔案路徑，但要呼叫launch中的參數對象，所以使用launch.substitutions.LaunchConfiguration('parameter_name')

    # xacro檔案可以使用xacro指令
    substitutions_command_result = launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')]) 
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result,value_type=str)

    # node robot_state_publisher啟動
    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher', # ros2 package名稱
        executable='robot_state_publisher', # 要執行的節點(可執行檔)
        parameters=[{'robot_description':robot_description_value}]
    )

    # node joint_state_publisher啟動
    action_joint_state_publisher = launch_ros.actions.Node(
        package='joint_state_publisher', # ros2 package名稱
        executable='joint_state_publisher', # 要執行的節點(可執行檔)
    )

    # 執行rviz2
    action_rviz_node = launch_ros.actions.Node(
        package='rviz2', # ros2 package名稱
        executable='rviz2', # 要執行的節點(可執行檔)
        arguments=['-d', default_rviz_config_path]
    )

    return launch.LaunchDescription([
        action_declate_arg_mode_path,
        action_robot_state_publisher,
        action_joint_state_publisher,
        action_rviz_node
    ])