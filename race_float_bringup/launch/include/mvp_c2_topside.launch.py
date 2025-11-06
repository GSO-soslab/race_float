import os
from launch import LaunchDescription
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


# from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_name = 'race_float'
    robot_bringup = robot_name + '_bringup'
    topside_setting_file = os.path.join(get_package_share_directory(robot_bringup), 'config', 'mvp_c2.yaml') 

    return LaunchDescription([
        Node(
            package = 'mvp_c2',
            namespace = robot_name,
            executable='mvp_c2_udp_comm',
            name = 'commander_c2_udp_comm',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[topside_setting_file],
            remappings=[
                ('dccl_msg_tx', 'mvp_c2/dccl_msg_tx'),
                ('dccl_msg_rx', 'mvp_c2/dccl_msg_rx'),
            ]
        ),
    #commander node
        Node(
            package='mvp_c2',
            namespace=robot_name,
            executable='mvp_c2_commander_ros',
            name='mvp_c2_commander',
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[topside_setting_file],
        ),
    ])