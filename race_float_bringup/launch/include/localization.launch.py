from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PythonExpression
from launch.actions import SetEnvironmentVariable
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
import os

def generate_launch_description():

    # Node argument
    robot_name = LaunchConfiguration('robot_name')
    localization_delay = LaunchConfiguration('localization_delay')
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Node param
    localization_param_file = Path(
        get_package_share_directory('race_float_bringup'), 
        'config/localization/robot_localization.yaml'
    )
     
    mag_model_path = os.path.join(
        get_package_share_directory('mvp_localization_utilities'), 
        'config/magnetic/'
    )

    init_file = Path(
        get_package_share_directory('race_float_bringup'), 
        'config/localization/robot_initialization.yaml'
    )    

    # Robot_Localization node
    # Publishes: /race_float/odometry/filtered
    # Subscribes: /vectornav/gps_odometry (from transform node)
    localization = Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            namespace=robot_name,
            # output='screen',
            parameters=[localization_param_file,
                        {'use_sim_time': use_sim_time}],
            emulate_tty=True        
    )

    # Initialization node (World Odom Transform)
    # 1. Takes /vectornav/gps/fix -> Publishes /vectornav/gps_odometry
    # 2. Takes /race_float/odometry/filtered -> Publishes /race_float/odometry/navsatfix
    initialization = Node(
            package='mvp_localization_utilities',
            executable='world_odom_transform_node',
            name='world_odom_transform_node',
            namespace=robot_name,
            output='screen',
            prefix=['stdbuf -o L'],
            parameters=[
                {'tf_prefix': robot_name},
                {'mag_model_path': mag_model_path},
                {'use_sim_time': use_sim_time},
                 init_file
            ],
            remappings=[
                        # Input from Bag (Raw GPS)
                        ('gps/fix', 'vectornav/gps/fix'),
                        
                        # Output to EKF (Metric GPS)
                        ('gps/odometry', 'vectornav/gps_odometry'),
                        
                        # Input from EKF (Fused Odometry)
                        ('odometry', 'odometry/filtered'),
                        
                        # Input from Bag (Depth)
                        ('depth', 'depth/odometry'),
                        ],
            emulate_tty=True        
    )

    return LaunchDescription([

        # Decalre arguments
        DeclareLaunchArgument(
            'robot_name', default_value = 'my_robot'            
        ),

        DeclareLaunchArgument(
            'localization_delay', default_value = '0.0'            
        ),

        DeclareLaunchArgument(
            'use_sim_time', default_value = 'false',
            description='Use simulation clock if true'
        ),

        # Delay the node if needed
        TimerAction(
            period=PythonExpression([localization_delay]),
            actions=[localization]
        ),

        TimerAction(
            period=PythonExpression([localization_delay]),
            actions=[initialization]
        ),                       
    ])