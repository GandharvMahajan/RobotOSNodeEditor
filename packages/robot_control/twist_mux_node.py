from PySide6.QtGui import QColor
from packages.base.node import BaseNode

class TwistMuxNode(BaseNode):
    """
    Node representing Twist Mux for velocity command prioritization.
    
    Multiplexer for prioritizing velocity commands from different sources.
    """
    def __init__(self):
        super().__init__(title="Twist Mux")
        
        # Set a distinctive color for robot control nodes
        self.body_color = QColor(180, 90, 90)  # Reddish
        self.header_color = QColor(160, 70, 70)
        
        # Add standard ports
        self.add_input_port("cmd_vel1")
        self.add_input_port("cmd_vel2")
        self.add_input_port("cmd_vel3")
        self.add_output_port("cmd_vel")
        
        # Update the node's appearance
        self.update() 