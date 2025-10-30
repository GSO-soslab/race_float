import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    robot_name = 'race_float'
    robot_bringup = robot_name + '_bringup'

    ld = LaunchDescription()

    param_config = os.path.join(
        get_package_share_directory(robot_bringup),
        'config',
        'sensors',
        'vectornav_vn300.yaml'
    )

    node = Node(
            package='vectornav_node',
            executable='driver',
            name='vectornav_node',
            output='screen',
            parameters=[param_config]
    )
    
    ld.add_action(node)

    return ld