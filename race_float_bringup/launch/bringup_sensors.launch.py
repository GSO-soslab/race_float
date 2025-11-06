import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    arg_robot_name = 'race_float'
    robot_bringup = arg_robot_name + '_bringup'

    #Pressure
    pressure = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','bluerobotics_bar30.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    # Unicore GPS
    vectornav_vn300 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(robot_bringup), 'launch','include','vectornav.launch.py')]),
        launch_arguments = {'arg_robot_name': arg_robot_name}.items()  
    )

    return LaunchDescription([
        vectornav_vn300,
        pressure
    ])