from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class NavigationNode(BaseNode):
    """
    Node representing navigation and mapping components for robot autonomy.
    
    Supports different navigation types:
    - nav2: Navigation stack that handles path planning and obstacle avoidance
    - slam_toolbox: Simultaneous Localization and Mapping for creating maps
    """
    def __init__(self, nav_type="nav2"):
        super().__init__(title=f"Navigation: {nav_type}")
        
        # Set a distinctive color for navigation nodes
        self.body_color = QColor(75, 180, 75)  # Green
        self.header_color = QColor(65, 160, 65)
        
        # Available navigation types
        self.nav_type = nav_type
        
        # Add standard ports based on the navigation type
        self.add_input_port("scan")
        self.add_input_port("odom")
        
        if nav_type == "nav2":
            self.add_input_port("goal_pose")
            self.add_output_port("cmd_vel")
            self.add_output_port("path")
        elif nav_type == "slam_toolbox":
            self.add_output_port("map")
            self.add_output_port("tf")
        
        # Update the node's appearance
        self.update() 