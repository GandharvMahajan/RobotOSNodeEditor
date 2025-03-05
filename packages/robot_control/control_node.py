from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class RobotControlNode(BaseNode):
    """
    Node representing robot control and actuation components.
    
    Supports different control types:
    - ros2_controllers: Hardware interface for controlling robot joints
    - twist_mux: Multiplexer for prioritizing velocity commands from different sources
    """
    def __init__(self, control_type="ros2_controllers"):
        super().__init__(title=f"Robot Control: {control_type}")
        
        # Set a distinctive color for robot control nodes
        self.body_color = QColor(180, 90, 90)  # Reddish
        self.header_color = QColor(160, 70, 70)
        
        # Available control types
        self.control_type = control_type
        
        # Add standard ports based on the control type
        if control_type == "ros2_controllers":
            self.add_input_port("joint_states")
            self.add_input_port("cmd_vel")
            self.add_output_port("joint_commands")
        elif control_type == "twist_mux":
            self.add_input_port("cmd_vel1")
            self.add_input_port("cmd_vel2")
            self.add_input_port("cmd_vel3")
            self.add_output_port("cmd_vel")
        
        # Update the node's appearance
        self.update() 