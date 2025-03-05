from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class ROS2ControllersNode(BaseNode):
    """
    Node representing ROS2 Controllers for robot control.
    
    Hardware interface for controlling robot joints.
    """
    def __init__(self):
        super().__init__(title="ROS2 Controllers")
        
        # Set a distinctive color for robot control nodes
        self.body_color = QColor(180, 90, 90)  # Reddish
        self.header_color = QColor(160, 70, 70)
        
        # Add standard ports
        self.add_input_port("joint_states")
        self.add_input_port("cmd_vel")
        self.add_output_port("joint_commands")
        
        # Update the node's appearance
        self.update() 