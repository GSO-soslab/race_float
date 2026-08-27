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
    gpio_delay = LaunchConfiguration('gpio_delay')

    # Node param
    parameters_file = Path(
        get_package_share_directory('race_float_bringup'), 
        'config/sensor/gpio_manager.yaml'
    )

    # GPIO Manager node
    node = Node(
        package='mvp_gpio_manager',
        executable='gpio_manager_node',
        name='gpio_manager',
        namespace=robot_name,
        output='screen',
        # prefix=['stdbuf -o L'],
        parameters=[parameters_file],
        emulate_tty=True        
    )    
    
    return LaunchDescription([

        # Decalre arguments
        DeclareLaunchArgument(
            'robot_name', default_value = 'my_robot'            
        ),

        DeclareLaunchArgument(
            'gpio_delay', default_value = '0.0'            
        ),

        # Delay the node if needed
        TimerAction(
            period=PythonExpression([gpio_delay]),
            actions=[node]
        ),
    ])