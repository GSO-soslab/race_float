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
    
    # PWM driver node
    node = Node(
        package='pwm_driver',
        executable='pwm_driver_node',
        name='pwm_driver_node',
        namespace=robot_name,
        output='screen',
        parameters=[parameters_file],      
        emulate_tty=True        
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