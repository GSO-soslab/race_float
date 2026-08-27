import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.actions import ExecuteProcess

def generate_launch_description():

    robot_name = 'race_float'

    # rmw_zenoh
    zenoh = ExecuteProcess(
            cmd=['ros2', 'run', 'rmw_zenoh_cpp', 'rmw_zenohd'],
            output='screen'
        )

    # Foxglove
    foxglove = IncludeLaunchDescription(
        XMLLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('race_float_bringup'),
                'launch/include/foxglove_bridge.launch.xml')),
        launch_arguments={
            'namespace': robot_name
        }.items()
    )

    # Power Monitor
    power = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/power_monitor.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'power_delay': '3.0'
        }.items()  
    )

    # Comuter Monitor
    computer = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/computer_monitor.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'computer_delay': '6.0'
        }.items()  
    ) 

    # GPIO manager
    gpio = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/gpio_manager.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'gpio_delay': '9.0'
        }.items()  
    ) 

    # PWM driver
    pwm = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/pwm_driver.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'pwm_delay': '12.0'
        }.items()  
    ) 

    return LaunchDescription([
        zenoh,
        foxglove,
        power,
        computer,
        gpio,
        pwm
    ])    