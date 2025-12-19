import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    robot_name = 'race_float'
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Vehicle description
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/description.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'description_delay': '0.0',
            'use_sim_time': use_sim_time
        }.items()  
    )

    # Vehicle localization
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/localization.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'localization_delay': '3.0',
            'use_sim_time': use_sim_time
        }.items()  
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value = 'false',
            description='Use simulation (Gazebo) clock if true'
        ),
        description,
        localization,
    ])