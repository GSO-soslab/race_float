import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource

def generate_launch_description():

    robot_name = 'race_float'

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

    # GPIO manager
    gpio = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/gpio_manager.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'gpio_delay': '3.0'
        }.items()  
    )    

    # Power Monitor
    power = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/power_monitor.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'power_delay': '6.0'
        }.items()  
    ) 

    # Comuter Monitor
    computer = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/computer_monitoring.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'computer_delay': '9.0'
        }.items()  
    ) 


    return LaunchDescription([
        foxglove,
        gpio,
        power,
        computer,
    ])    