import launch
import launch.event_handlers
import launch_ros
from ament_index_python.packages import get_package_share_directory # 尋找目錄用
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

import launch_ros.parameter_descriptions

def generate_launch_description():
    # 獲取功能包的share路徑
    urdf_package_path = get_package_share_directory('fishbot_description')
    default_xacro_path = os.path.join(urdf_package_path,'urdf','fish_bot/fish_robot.urdf.xacro')
    # default_rviz_config_path = os.path.join(urdf_package_path,'config','display_robot_model.rviz')
    # 設定world文件目錄
    default_gazebo_world_path = os.path.join(urdf_package_path,'world','map9x9.world')

    action_declate_arg_mode_path = launch.actions.DeclareLaunchArgument(
        name='model',                           # 參數名稱
        default_value=str(default_xacro_path),   # 預設值(可選)
        description='加載的模型文件路徑'            # 參數描述(可選)
    )

    substitutions_command_result = launch.substitutions.Command(['xacro ',launch.substitutions.LaunchConfiguration('model')]) 
    robot_description_value = launch_ros.parameter_descriptions.ParameterValue(substitutions_command_result,value_type=str)

    action_robot_state_publisher = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description':robot_description_value}]
    )

    # 啟動gazebo，啟用gazebo官方給予的launch文件
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        PythonLaunchDescriptionSource([get_package_share_directory(
            'gazebo_ros'), '/launch', '/gazebo.launch.py']),
      	# 传递参数
        launch_arguments=[('world', default_gazebo_world_path),('verbose','true')]
    )

    action_spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        # 透過話題讓gazebo開啟urdf機器人模型
        # topic選傳參數：參數名稱 entity必傳參數：機器人名稱
        arguments=['-topic','/robot_description','-entity','fishbot']
    )

    action_load_joint_state_controller = launch.actions.ExecuteProcess(
        cmd='ros2 control load_controller fishbot_joint_state_broadcaster --set-state active'.split(' '),
        output='screen'
    )

    # 力控制器也能控制輪子進行轉動，最好不要與下方的兩輪差速控制器一同使用
    # action_load_effort_state_controller = launch.actions.ExecuteProcess(
    #     cmd='ros2 control load_controller fishbot_effort_controller --set-state active'.split(' '),
    #     output='screen'
    # )

    action_load_diff_driver_controller = launch.actions.ExecuteProcess(
        cmd='ros2 control load_controller fishbot_diff_drive_controller --set-state active'.split(' '),
        output='screen'
    )

    # 模擬機器人關節與角度
    # action_joint_state_publisher = launch_ros.actions.Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    # )

    # 執行rviz2
    # action_rviz_node = launch_ros.actions.Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     arguments=['-d', default_rviz_config_path]
    # )

    return launch.LaunchDescription([
        action_declate_arg_mode_path,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_spawn_entity,
                on_exit=[action_load_joint_state_controller],
            )
        ),

        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action=action_load_joint_state_controller,
        #         on_exit=[action_load_effort_state_controller],
        #     )
        # ),

        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=action_load_joint_state_controller,
                on_exit=[action_load_diff_driver_controller],
            )
        ),
        # action_joint_state_publisher,
        # action_rviz_node
    ])