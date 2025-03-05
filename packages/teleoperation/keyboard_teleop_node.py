from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class KeyboardTeleopNode(BaseNode):
    """
    Node representing keyboard-based teleoperation for robot control.
    
    Publishes velocity commands based on keyboard input.
    """
    def __init__(self):
        super().__init__(title="Keyboard Teleop")
        
        # Set a distinctive color for teleoperation nodes
        self.body_color = QColor(70, 130, 180)  # Steel blue
        self.header_color = QColor(60, 110, 160)
        
        # Add standard ports
        self.add_output_port("cmd_vel")
        
        # Update the node's appearance
        self.update() 