from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class JoystickTeleopNode(BaseNode):
    """
    Node representing joystick-based teleoperation for robot control.
    
    Subscribes to joy messages and publishes velocity commands.
    """
    def __init__(self):
        super().__init__(title="Joystick Teleop")
        
        # Set a distinctive color for teleoperation nodes
        self.body_color = QColor(70, 130, 180)  # Steel blue
        self.header_color = QColor(60, 110, 160)
        
        # Add standard ports
        self.add_input_port("joy")
        self.add_output_port("cmd_vel")
        
        # Update the node's appearance
        self.update() 