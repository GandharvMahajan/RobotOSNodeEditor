from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class SlamToolboxNode(BaseNode):
    """
    Node representing the SLAM Toolbox for mapping.
    
    Handles Simultaneous Localization and Mapping for creating maps.
    """
    def __init__(self):
        super().__init__(title="SLAM Toolbox")
        
        # Set a distinctive color for navigation nodes
        self.body_color = QColor(75, 180, 75)  # Green
        self.header_color = QColor(65, 160, 65)
        
        # Add standard ports
        self.add_input_port("scan")
        self.add_input_port("odom")
        self.add_output_port("map")
        self.add_output_port("tf")
        
        # Update the node's appearance
        self.update() 