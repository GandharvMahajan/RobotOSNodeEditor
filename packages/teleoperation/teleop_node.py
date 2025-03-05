from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class TeleoperationNode(BaseNode):
    """
    Node representing teleoperation components for robot control.
    
    Supports different teleoperation types:
    - teleop_twist_keyboard: Keyboard-based control that publishes cmd_vel
    - teleop_twist_joy: Joystick-based control that subscribes to joy and publishes cmd_vel
    """
    def __init__(self, teleop_type="teleop_twist_keyboard"):
        super().__init__(title=f"Teleoperation: {teleop_type}")
        
        # Set a distinctive color for teleoperation nodes
        self.body_color = QColor(70, 130, 180)  # Steel blue
        self.header_color = QColor(60, 110, 160)
        
        # Available teleop types
        self.teleop_type = teleop_type
        
        # Add standard ports based on the teleop type
        self.add_output_port("cmd_vel")
        
        if teleop_type == "teleop_twist_joy":
            self.add_input_port("joy")
        elif teleop_type == "teleop_twist_keyboard":
            pass  # No inputs for keyboard teleop
        
        # Update the node's appearance
        self.update() 