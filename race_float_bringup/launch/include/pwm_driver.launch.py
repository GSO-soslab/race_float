# import os
# import yaml
# import pathlib
# from launch import LaunchDescription
# import launch.actions
# from ament_index_python.packages import get_package_share_directory
# from launch_ros.actions import Node
# from launch.substitutions import EnvironmentVariable
# from launch.actions import DeclareLaunchArgument

# def generate_launch_description():
#     robot_name = 'race_float'
#     robot_bringup = robot_name + '_bringup'

#     ld = LaunchDescription()

#     param_config = os.path.join(
#         get_package_share_directory(robot_bringup),
#         'config',
#         'sensor',
#         'pwm_driver.yaml'
#     )

#     node = Node(
#             package='pwm_driver',
#             namespace=robot_name,
#             executable='pwm_driver_node',
#             name='pwm_driver_node',
#             prefix=['stdbuf -o L'],
#             output="screen",
#             parameters=[param_config]
#             )

#     ld.add_action(node)

#     return ld

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.actions import SetEnvironmentVariable
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path

def generate_launch_description():

    # Node argument
    robot_name = LaunchConfiguration('robot_name')
    pwm_delay = LaunchConfiguration('pwm_delay')

    # Node param
    parameters_file = Path(
        get_package_share_directory('race_float_bringup'), 
        'config/sensor/pwm_driver.yaml'
    )

    # GPIO Manager node
    node = Node(
        package='pwm_driver',
        executable='pwm_driver_node',
        name='pwm_driver_node',
        namespace=robot_name,
        output='screen',
        # prefix=['stdbuf -o L'],
        parameters=[parameters_file],
    )    
    
    return LaunchDescription([

        # Decalre arguments
        DeclareLaunchArgument(
            'robot_name', default_value = 'my_robot'            
        ),

        DeclareLaunchArgument(
            'pwm_delay', default_value = '0.0'            
        ),

        # Delay the node if needed
        TimerAction(
            period=PythonExpression([pwm_delay]),
            actions=[node]
        ),
    ])