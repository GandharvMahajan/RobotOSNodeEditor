from PySide6.QtWidgets import QGraphicsScene, QGraphicsPathItem, QMenu, QGraphicsSceneMouseEvent
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainterPath, QPen, QColor, QTransform, QBrush

from packages.base.node import BaseNode, Port
from connection import Connection

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
        # Create menu
        menu = QMenu()
        
        # Teleoperation submenu
        teleop_menu = menu.addMenu("Teleoperation")
        keyboard_action = teleop_menu.addAction("Keyboard Teleop")
        joy_action = teleop_menu.addAction("Joystick Teleop")
        
        # Navigation submenu
        nav_menu = menu.addMenu("Navigation & Mapping")
        nav2_action = nav_menu.addAction("Nav2")
        slam_action = nav_menu.addAction("SLAM Toolbox")
        
        # Control submenu
        control_menu = menu.addMenu("Robot Control")
        ros2_control_action = control_menu.addAction("ROS2 Controllers")
        twist_mux_action = control_menu.addAction("Twist Mux")
        
        # Get the first view
        if not self.views():
            return
        view = self.views()[0]
        
        # Convert scene position to global screen coordinates
        viewport_pos = view.mapFromScene(position)
        global_pos = view.viewport().mapToGlobal(viewport_pos)
        
        # Execute menu at the correct position
        action = menu.exec_(global_pos)
        
        # Process result
        if action == keyboard_action:
            print("Creating Keyboard Teleop node")
            node = KeyboardTeleopNode()
            node.setPos(position)
            self.addItem(node)
        elif action == joy_action:
            print("Creating Joystick Teleop node")
            node = JoystickTeleopNode()
            node.setPos(position)
            self.addItem(node)
        elif action == nav2_action:
            print("Creating Nav2 node")
            node = Nav2Node()
            node.setPos(position)
            self.addItem(node)
        elif action == slam_action:
            print("Creating SLAM Toolbox node")
            node = SlamToolboxNode()
            node.setPos(position)
            self.addItem(node)
        elif action == ros2_control_action:
            print("Creating ROS2 Controllers node")
            node = ROS2ControllersNode()
            node.setPos(position)
            self.addItem(node)
        elif action == twist_mux_action:
            print("Creating Twist Mux node")
            node = TwistMuxNode()
            node.setPos(position)
            self.addItem(node)