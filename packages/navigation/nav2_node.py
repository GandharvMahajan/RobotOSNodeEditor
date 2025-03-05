from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class Nav2Node(BaseNode):
    """
    Node representing the Nav2 navigation stack.
    
    Handles path planning, obstacle avoidance, and robot navigation.
    """
    def __init__(self):
        super().__init__(title="Nav2")
        
        # Set a distinctive color for navigation nodes
        self.body_color = QColor(75, 180, 75)  # Green
        self.header_color = QColor(65, 160, 65)
        
        # Add standard ports
        self.add_input_port("scan")
        self.add_input_port("odom")
        self.add_input_port("goal_pose")
        self.add_output_port("cmd_vel")
        self.add_output_port("path")
        
        # Update the node's appearance
        self.update()
        
    def on_start(self):
        """Called when the node is started"""
        print(f"Starting navigation node: {self.title}")
        # In a real implementation, this would:
        # 1. Initialize the navigation stack
        # 2. Start subscribing to sensor topics
        # 3. Set up the navigation parameters
        # 4. Begin processing navigation requests
        
    def on_stop(self):
        """Called when the node is stopped"""
        print(f"Stopping navigation node: {self.title}")
        # In a real implementation, this would:
        # 1. Stop the navigation stack
        # 2. Unsubscribe from sensor topics
        # 3. Send zero velocity commands to stop the robot
        # 4. Clean up any resources 