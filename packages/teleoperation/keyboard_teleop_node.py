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
        
    def on_start(self):
        """Called when the node is started"""
        print(f"Starting keyboard teleoperation node: {self.title}")
        # In a real implementation, this would:
        # 1. Start listening for keyboard events
        # 2. Initialize any required resources
        # 3. Set up connections to ROS or other systems
        
    def on_stop(self):
        """Called when the node is stopped"""
        print(f"Stopping keyboard teleoperation node: {self.title}")
        # In a real implementation, this would:
        # 1. Stop listening for keyboard events
        # 2. Release any resources
        # 3. Clean up connections to ROS or other systems 