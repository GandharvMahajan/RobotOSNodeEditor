from PySide6.QtWidgets import QGraphicsScene, QGraphicsPathItem, QMenu, QGraphicsSceneMouseEvent
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainterPath, QPen, QColor, QTransform, QBrush

from packages.base.node import BaseNode, Port
from connection import Connection
from node_menu import NodeSearchMenu

# Import specific node types from their respective packages
from packages.teleoperation import KeyboardTeleopNode, JoystickTeleopNode
from packages.navigation import Nav2Node, SlamToolboxNode
from packages.robot_control import ROS2ControllersNode, TwistMuxNode


class NodeScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(0, 0, 8000, 8000)  # Set a large scene rect by default
        
        # Track connection creation
        self.current_connection = None
        self.start_port = None
        self.is_creating_connection = False  # Flag to track connection creation state
        
        # Keep track of all connections for easy access
        self.connections = []
        
        # Add grid (optional)
        self.grid_size = 20
        self.grid_pen = QPen(QColor(60, 60, 60), 0.5)
        
        # Set a background color
        self.setBackgroundBrush(QBrush(QColor(40, 40, 40)))
    
    def startConnection(self, start_port):
        """Start creating a connection from the given output port"""
        self.start_port = start_port
        self.is_creating_connection = True
        
        # Create a temporary connection
        self.current_connection = Connection(start_port)
        self.addItem(self.current_connection)
        
    def mouseMoveEvent(self, event):
        # If we're creating a connection, update the endpoint to follow the mouse
        if self.is_creating_connection and self.current_connection:
            self.current_connection.updateEndPoint(event.scenePos())
            event.accept()
            return
            
        # Otherwise, pass to the base handler
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        # If we're creating a connection, finish it
        if self.is_creating_connection and self.current_connection:
            # Try to find a port at the release point
            end_port = self.findPortAt(event.scenePos())
            
            if end_port and end_port.is_input and end_port.node != self.start_port.node:
                # We found a valid input port that's not on the same node
                
                # Finalize the connection
                self.current_connection.setEndPort(end_port)
                
                # Add to our list of connections
                self.connections.append(self.current_connection)
            else:
                # No valid end port found, remove the temporary connection
                self.removeItem(self.current_connection)
            
            # Reset state
            self.current_connection = None
            self.start_port = None
            self.is_creating_connection = False
            
            # Accept the event to prevent further processing
            event.accept()
            return
        
        super().mouseReleaseEvent(event)

    def findPortAt(self, scene_pos):
        items = self.items(scene_pos)
        for item in items:
            if hasattr(item, 'input_ports'):  # Check if it's a node
                # Check input ports
                for port in item.input_ports.values():
                    port_pos = item.mapToScene(port.relative_pos)
                    if (port_pos - scene_pos).manhattanLength() < 10:
                        return port
                # Check output ports
                for port in item.output_ports.values():
                    port_pos = item.mapToScene(port.relative_pos)
                    if (port_pos - scene_pos).manhattanLength() < 10:
                        return port
        return None

    def mousePressEvent(self, event):
        """Handle mouse press events in the scene"""
        # First check if we clicked on a port
        port = self.findPortAt(event.scenePos())
        if port:
            # If it's an output port, start a connection
            if not port.is_input:
                self.startConnection(port)
                event.accept()
                return
            # Input ports just consume the event without doing anything
            else:
                event.accept()
                return
            
        # If not on a port, check if we're clicking on a node
        items = self.items(event.scenePos())
        for item in items:
            if isinstance(item, BaseNode):
                # Pass the event to the standard handler which will pass it to the node
                super().mousePressEvent(event)
                return
        
        # If right-click and not on a node or port, show context menu
        if event.button() == Qt.RightButton:
            self.showContextMenu(event.scenePos())
            event.accept()
            return
            
        # Clear selection for background clicks (unless holding Shift)
        if not (event.modifiers() & Qt.ShiftModifier):
            self.clearSelection()

        # Pass the event to the base class
        super().mousePressEvent(event)

    def showContextMenu(self, position):
        """Show a context menu at the given scene position"""
        # Create custom menu with search
        menu = NodeSearchMenu()
        
        # Add function category with utility actions
        menu.add_node_action("Functions", "Add node button", None)
        
        # Add package categories and actions
        # Teleoperation nodes
        menu.add_node_action("Packages/Teleoperation", "Keyboard Teleop", KeyboardTeleopNode, submenu=True)
        menu.add_node_action("Packages/Teleoperation", "Joystick Teleop", JoystickTeleopNode, submenu=True)
        
        # Navigation nodes
        menu.add_node_action("Packages/Navigation & Mapping", "Nav2", Nav2Node, submenu=True)
        menu.add_node_action("Packages/Navigation & Mapping", "SLAM Toolbox", SlamToolboxNode, submenu=True)
        
        # Control nodes
        menu.add_node_action("Packages/Robot Control", "ROS2 Controllers", ROS2ControllersNode, submenu=True)
        menu.add_node_action("Packages/Robot Control", "Twist Mux", TwistMuxNode, submenu=True)
        
        # Get the first view
        if not self.views():
            return
        view = self.views()[0]
        
        # Convert scene position to global screen coordinates
        viewport_pos = view.mapFromScene(position)
        global_pos = view.viewport().mapToGlobal(viewport_pos)
        
        # Execute menu at the correct position
        action = menu.exec_(global_pos)
        
        # Process result - find which node was selected
        if action:
            for node_name, node_info in menu.all_node_actions.items():
                if node_info['action'] == action:
                    if node_name == "Add node button":
                        # Handle the Add node button action
                        print("Add node button clicked")
                        # TODO: Implement functionality for adding a node button
                    else:
                        print(f"Creating {node_name} node")
                        node = node_info['node_class']()
                        node.setPos(position)
                        self.addItem(node)
                    break