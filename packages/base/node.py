from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import QRectF, QPointF, Qt
from PySide6.QtGui import QPainter, QBrush, QPen, QColor, QFont

class Port:
    def __init__(self, node, name, is_input=True):
        self.node = node
        self.name = name
        self.is_input = is_input
        self.connections = []  # List of connections attached to this port
        self.relative_pos = QPointF(0, 0)  # Will be set by node
        self.radius = node.port_radius if hasattr(node, 'port_radius') else 8  # Port radius

    def get_scene_pos(self):
        """Get the port position in scene coordinates"""
        if not self.node or not self.node.scene():
            return QPointF(0, 0)
        return self.node.mapToScene(self.relative_pos)

    def contains_point(self, point):
        """Check if the given point (in node coordinates) is within the port circle"""
        port_center = self.relative_pos
        diff = point - port_center
        return (diff.x() * diff.x() + diff.y() * diff.y()) <= (self.radius * self.radius)

    def disconnect_all(self):
        """Disconnect all connections from this port"""
        # Create a copy of the list since we'll be modifying it
        connections_copy = self.connections.copy()
        for connection in connections_copy:
            connection.disconnectFromPorts()

    def get_connected_nodes(self):
        """Get a list of all nodes connected to this port via connections"""
        connected_nodes = []
        for connection in self.connections:
            if connection.start_port and connection.start_port != self:
                connected_nodes.append(connection.start_port.node)
            elif connection.end_port and connection.end_port != self:
                connected_nodes.append(connection.end_port.node)
        return connected_nodes

class BaseNode(QGraphicsItem):
    def __init__(self, title="Base Node"):
        super().__init__()
        
        # Set basic flags - these determine how the item can be interacted with
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        
        # Visual properties
        self.width = 180
        self.header_height = 40
        self.height = 120
        self.port_spacing = 30
        self.port_radius = 8
        self.title = title
        
        # Colors
        self.body_color = QColor(60, 60, 80)      # Dark blue-gray base color
        self.header_color = QColor(50, 50, 70)    # Slightly darker for header
        self.selected_color = QColor(80, 100, 120) # Lighter when selected
        self.text_color = QColor(220, 220, 220)   # Light gray for text
        self.port_color = QColor(180, 180, 180)   # Light gray for ports
        self.border_color = QColor(100, 100, 100) # Medium gray for borders
        self.run_button_color = QColor(50, 180, 50)  # Green for run
        self.stop_button_color = QColor(180, 50, 50)  # Red for stop
        
        # Port management
        self.input_ports = {}
        self.output_ports = {}
        
        # Interaction state
        self.port_under_mouse = None
        self._dragging = False
        self._drag_start_pos = QPointF()
        
        # Run/Stop button properties
        self.is_running = False
        self.button_size = 20
        self.button_margin = 10
        
        # Accept hover events
        self.setAcceptHoverEvents(True)

    def add_input_port(self, name):
        port = Port(self, name, is_input=True)
        self.input_ports[name] = port
        self._update_port_positions()
        return port
        
    def add_output_port(self, name):
        port = Port(self, name, is_input=False)
        self.output_ports[name] = port
        self._update_port_positions()
        return port
        
    def _update_port_positions(self):
        # Position input ports on the left edge
        for i, port in enumerate(self.input_ports.values()):
            port.relative_pos = QPointF(0, self.header_height + (i + 1) * self.port_spacing)
            
        # Position output ports on the right edge
        for i, port in enumerate(self.output_ports.values()):
            port.relative_pos = QPointF(self.width, self.header_height + (i + 1) * self.port_spacing)
            
        # Update node height based on number of ports
        num_ports = max(len(self.input_ports), len(self.output_ports))
        self.height = max(120, self.header_height + (num_ports + 1) * self.port_spacing)

    def boundingRect(self):
        # Add some padding to the bounding rect to prevent artifacts
        padding = 10
        return QRectF(-padding, -padding, 
                     self.width + 2*padding, 
                     self.height + 2*padding)

    def toggle_run_state(self):
        """Toggle the run/stop state of the node"""
        self.is_running = not self.is_running
        self.update()  # Trigger repaint
        
        # Implement any additional logic when the state changes
        if self.is_running:
            self.on_start()
        else:
            self.on_stop()
    
    def on_start(self):
        """Called when the node is started"""
        # Override in subclasses to implement specific start behavior
        pass
    
    def on_stop(self):
        """Called when the node is stopped"""
        # Override in subclasses to implement specific stop behavior
        pass
    
    def get_button_rect(self):
        """Get the rectangle for the run/stop button"""
        return QRectF(
            self.width - self.button_size - self.button_margin,
            self.height - self.button_size - self.button_margin,
            self.button_size,
            self.button_size
        )
    
    def is_point_in_button(self, point):
        """Check if the given point is within the run/stop button"""
        return self.get_button_rect().contains(point)

    def mousePressEvent(self, event):
        """Handle mouse press events on the node"""
        # Check if we clicked on the run/stop button
        if self.is_point_in_button(event.pos()):
            self.toggle_run_state()
            event.accept()
            return
            
        # Store the original position for potential dragging
        self._drag_start_pos = event.pos()
        
        # Check if we clicked on a port
        port = self.port_at_position(event.pos())
        if port:
            # If it's an output port, start a connection - don't move the node
            if not port.is_input and self.scene():
                self.scene().startConnection(port)
                # Important: Don't start dragging when creating a connection
                self._dragging = False
                event.accept()
                return
            # For input ports, just prevent dragging
            elif port.is_input:
                # Don't start dragging when clicking on an input port
                self._dragging = False
                event.accept()
                return
        
        # Handle selection based on modifier keys
        if event.modifiers() & Qt.ShiftModifier:
            # Toggle selection with Shift
            self.setSelected(not self.isSelected())
        else:
            # If not using Shift, clear other selections unless this is the only selected item
            scene = self.scene()
            if scene:
                selected_items = scene.selectedItems()
                if len(selected_items) != 1 or selected_items[0] != self:
                    scene.clearSelection()
                    self.setSelected(True)  # Select this node
        
        # Prepare for dragging
        self._dragging = True
        self.setCursor(Qt.ClosedHandCursor)
        
        # Let the base class handle the rest
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse movement on the node"""
        # Only handle dragging if we're not creating a connection
        if self._dragging:
            # Calculate the new position
            new_pos = self.mapToScene(event.pos() - self._drag_start_pos)
            self.setPos(new_pos)
            
            # Update connections
            self.updateConnections()
            
            event.accept()
            return
            
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events on the node"""
        # Only handle release if we were dragging
        if self._dragging:
            self._dragging = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
            
        # Let the base class handle the rest
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        # Update connections when node is moved
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.updateConnections()
            
        # When selection state changes, make sure we're properly handling group selection
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            if value:  # If being selected
                # If we're being selected and not due to Shift key,
                # we've already cleared other selections in mousePressEvent
                pass
                
        return super().itemChange(change, value)

    def updateConnections(self):
        """Update all connections attached to this node's ports without moving nodes"""
        # Store original selected items state to restore it after updates
        scene = self.scene()
        if not scene:
            return
            
        # Look for existing connections in the port's connection list and update them
        # Input ports
        for port_name, port in self.input_ports.items():
            for connection in port.connections:
                connection.updatePath()
        
        # Output ports
        for port_name, port in self.output_ports.items():
            for connection in port.connections:
                connection.updatePath()

    def port_at_position(self, pos):
        # Check input ports
        for port in self.input_ports.values():
            if port.contains_point(pos):
                return port
                
        # Check output ports
        for port in self.output_ports.values():
            if port.contains_point(pos):
                return port
        
        return None

    def hoverMoveEvent(self, event):
        # Update port highlighting
        port = self.port_at_position(event.pos())
        if port != self.port_under_mouse:
            self.port_under_mouse = port
            self.update()  # Trigger repaint
        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        # Clear port highlighting
        self.port_under_mouse = None
        self.update()
        super().hoverLeaveEvent(event)

    def paint(self, painter, option, widget):
        # Draw node body
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Define colors based on selection state
        body_color = self.selected_color if self.isSelected() else self.body_color
        
        # Draw main body
        painter.setPen(QPen(self.border_color, 1))
        painter.setBrush(QBrush(body_color))
        painter.drawRoundedRect(0, 0, self.width, self.height, 5, 5)
        
        # Draw header
        painter.setBrush(QBrush(self.header_color))
        painter.drawRoundedRect(0, 0, self.width, self.header_height, 5, 5)
        painter.drawRect(0, self.header_height - 5, self.width, 5)  # Bottom of header
        
        # Draw title
        painter.setPen(QPen(self.text_color))
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(10, 25, self.title)
        
        # Draw ports
        for port in self.input_ports.values():
            # Determine port color based on hover state
            if port == self.port_under_mouse:
                painter.setBrush(QColor(200, 200, 200))  # Lighter color for hover
            else:
                painter.setBrush(self.port_color)
            
            painter.setPen(QPen(self.border_color, 1))
            # Draw port circle centered at the port's relative position
            painter.drawEllipse(port.relative_pos, port.radius, port.radius)
            
            # Draw port name
            painter.setPen(QPen(self.text_color))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(port.relative_pos.x() + 10, port.relative_pos.y() + 4, port.name)
        
        for port in self.output_ports.values():
            # Determine port color based on hover state
            if port == self.port_under_mouse:
                painter.setBrush(QColor(200, 200, 200))  # Lighter color for hover
            else:
                painter.setBrush(self.port_color)
            
            painter.setPen(QPen(self.border_color, 1))
            # Draw port circle centered at the port's relative position
            painter.drawEllipse(port.relative_pos, port.radius, port.radius)
            
            # Draw port name (right-aligned)
            painter.setPen(QPen(self.text_color))
            painter.setFont(QFont("Arial", 8))
            text_width = painter.fontMetrics().horizontalAdvance(port.name)
            painter.drawText(port.relative_pos.x() - text_width - 10, port.relative_pos.y() + 4, port.name)
            
        # Draw run/stop button
        button_rect = self.get_button_rect()
        button_color = self.run_button_color if self.is_running else self.stop_button_color
        painter.setBrush(QBrush(button_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(button_rect, 3, 3)
        
        # Draw button text
        painter.setPen(QPen(self.text_color))
        painter.setFont(QFont("Arial", 8, QFont.Bold))
        button_text = "RUN" if not self.is_running else "STOP"
        text_width = painter.fontMetrics().horizontalAdvance(button_text)
        text_height = painter.fontMetrics().height()
        text_x = button_rect.x() + (button_rect.width() - text_width) / 2
        text_y = button_rect.y() + (button_rect.height() + text_height) / 2 - 2
        painter.drawText(text_x, text_y, button_text) 