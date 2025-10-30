import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    robot_name = 'race_float'

    # Vehicle description
    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('race_float_bringup'), 
            'launch/include/description.launch.py')]),
        launch_arguments={
            'robot_name': robot_name,
            'description_delay': '0.0'
        }.items()  
    )

    return LaunchDescription([
        description,
    ])