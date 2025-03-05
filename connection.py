from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen, QColor
from PySide6.QtCore import Qt, QPointF

class Connection(QGraphicsPathItem):
    def __init__(self, start_port, end_port=None):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.end_point = start_port.get_scene_pos()
        
        # Visual properties
        self.pen_width = 2
        self.pending_color = QColor(200, 200, 50, 150)  # Yellow for pending connections
        self.complete_color = QColor(100, 180, 255)     # Blue for complete connections
        
        # Set default pen
        self.setPen(QPen(self.pending_color, self.pen_width))
        
        # Add to start port's connections list
        if start_port and not self in start_port.connections:
            start_port.connections.append(self)
        
        # Add to end port's connections list if applicable
        if end_port and not self in end_port.connections:
            end_port.connections.append(self)
        
        # Make sure connections aren't selectable to avoid interfering with node selection
        self.setFlag(QGraphicsPathItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsPathItem.ItemIsMovable, False)  # Connections shouldn't be movable
        
        # Prevent connections from accepting any mouse button events
        self.setAcceptedMouseButtons(Qt.NoButton)
        
        # Update the path
        self.updatePath()
        
        # Ensure connection stays below nodes
        self.setZValue(-1)

    def mousePressEvent(self, event):
        """Override to prevent any mouse press interaction"""
        # Connections should not respond to mouse presses
        event.ignore()

    def mouseMoveEvent(self, event):
        """Override to prevent any mouse move interaction"""
        # Connections should not respond to mouse movement
        event.ignore()
        
    def mouseReleaseEvent(self, event):
        """Override to prevent any mouse release interaction"""
        # Connections should not respond to mouse releases
        event.ignore()

    def updatePath(self):
        """Update the connection's path based on the current port positions"""
        # Get the current positions
        start_pos = self.start_port.get_scene_pos() if self.start_port else QPointF(0, 0)
        end_pos = self.end_port.get_scene_pos() if self.end_port else self.end_point
        
        # Create the path
        path = QPainterPath(start_pos)
        
        # Calculate horizontal offset for control points (at least 100 pixels)
        ctrl_distance = max(100, abs(end_pos.x() - start_pos.x()) * 0.5)
        
        # Create a curved path
        ctrl1 = QPointF(start_pos.x() + ctrl_distance, start_pos.y())
        ctrl2 = QPointF(end_pos.x() - ctrl_distance, end_pos.y())
        path.cubicTo(ctrl1, ctrl2, end_pos)
        
        # Update the path
        self.setPath(path)

    def updateEndPoint(self, pos):
        """Update the end point for an in-progress connection"""
        self.end_point = pos
        self.updatePath()

    def setEndPort(self, end_port):
        """Set the end port for this connection"""
        # Remove from old end port, if any
        if self.end_port and self in self.end_port.connections:
            self.end_port.connections.remove(self)
            
        # Set new end port
        self.end_port = end_port
        
        # Add to new end port
        if end_port and not self in end_port.connections:
            end_port.connections.append(self)
            
        # Update visual style for completed connection
        self.setPen(QPen(self.complete_color, self.pen_width))
        
        # Update path
        self.updatePath()

    def disconnectFromPorts(self):
        """Remove this connection from its ports"""
        # Remove from start port
        if self.start_port and self in self.start_port.connections:
            self.start_port.connections.remove(self)
            
        # Remove from end port
        if self.end_port and self in self.end_port.connections:
            self.end_port.connections.remove(self)
            
        # Clear references
        self.start_port = None
        self.end_port = None
        
    def __del__(self):
        """Ensure connections are properly removed when the object is deleted"""
        self.disconnectFromPorts()